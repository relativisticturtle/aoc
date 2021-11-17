from collections import deque
import os
import sys
import warnings
import argparse

import IntCode

class NodeFunction:
    def __init__(self, fname, parameters, block):
        self.fname = fname
        self.parameters = parameters
        self.block = block

        # Local variables from function body
        self.stack_size = self.block.setup_variables_on_stack(0) + len(self.parameters)

        # Parameters (treated like local variables)
        rbo = -self.stack_size
        for param in self.parameters:
            param.address = rbo
            rbo += 1
    
    def emit(self, global_variables):
        precode = []
        
        # Allocate memory on stack for return address, parameters and local variables
        #   (RB[0]-address: +1, return address: +1)
        rbo_step = 2 + self.stack_size
        precode.append(['<FCN_%s>' % self.fname, 'ARB', rbo_step])
        precode.append(['<RB_new=RB_old+%d>' % rbo_step, 'ADD', 'RB[%d]' % -rbo_step, rbo_step, 'RB[0]'])
        
        # Emit code body
        precode.extend(self.block.emit(global_variables + self.parameters, return_location='</FCN_%s>' % self.fname))
        # Restore stack (parameters and return address are also consumed)
        precode.append(['</FCN_%s>' % self.fname, 'ARB', -rbo_step])
        # Jump to designated return location
        precode.append([None, 'JZ', 0, 'RB[1]'])

        return precode


class NodeScope:
    def __init__(self, children, local_variables):
        self.local_variables = local_variables
        self.subscopes = [c for c in children if isinstance(c, NodeScope)]

    def setup_variables_on_stack(self, stack_size):
        for variable in self.local_variables:
            stack_size += 1 + int(variable.array_size) if variable.array_size else 1
            variable.address = -stack_size
        max_stack_size = stack_size
        for subscope in self.subscopes:
            max_stack_size = max(max_stack_size, subscope.setup_variables_on_stack(stack_size))
        return max_stack_size
    
    def emit(self):
        # Setup all local array variables
        precode = []
        for v in self.local_variables:
            if v.array_size and v.array_size > 0:
                precode.append(['<int %s[]>' % v.name, 'ADD', 0, v.address + 1, 'RB[%d]' % v.address])
        return precode


class NodeProgram:
    def __init__(self, functions, global_variables):
        self.global_variables = global_variables
        self.functions = functions

        for v in self.global_variables:
            v.address = '<global_%s>' % v.name


    def emit(self):
        # --- HEADER ---
        precode = []
        precode.append(['<CODE>', 'ARB', '<STACK/>'])
        precode.append(['<RB=...>', 'ADD', 0, '<STACK/>', 'RB[0]'])

        # Call main
        node_call = NodeCall('main', [])
        precode.extend(node_call.emit([]))

        # Stop
        precode.append(['<STOP>', 'STOP'])
        
        # --- CODE ---
        for node_fcn in functions:
            precode.extend(node_fcn.emit(self.global_variables))

        # --- STOP ---
        precode.append(['</CODE>', 'STOP'])

        # --- DATA SECTION ---
        
        # Setup all global variables
        for v in self.global_variables:
            # v.address = '<global_%s>' % v.name
            if v.array_size and v.array_size > 0:
                precode.append(['<global_%s>' % v.name, '<global_%s> + 1' % v.name])
                if v.array_init is not None and len(v.array_init) <= v.array_size:
                    precode.append(['<  [%d]>' % v.array_size, *(v.array_init + [0] * (v.array_size - len(v.array_init)))])
                elif v.array_init is None:
                    precode.append(['<  [%d]>' % v.array_size, *([0] * v.array_size)])
                else:
                    raise SyntaxError('Array cannot hold all that')
            else:
                precode.append(['<global_%s>' % v.name, 0])
        
        precode.append(['<STACK/>', 0])
        return precode


class NodeBlock(NodeScope):
    def __init__(self, statements, local_variables):
        super(NodeBlock, self).__init__(statements, local_variables)
        self.statements = statements

    def emit(self, local_variables, **kwargs):
        # Emit code for this scope's local variables
        precode = super(NodeBlock, self).emit()
        
        # Delegate to statements
        for statement in self.statements:
            precode.extend(statement.emit(local_variables + self.local_variables, **kwargs))
        return precode


class NodeIfElse(NodeScope):
    _num = 0
    def __init__(self, condition, iftrue, iffalse=None):
        super(NodeIfElse, self).__init__([iftrue, iffalse], [])
        NodeIfElse._num += 1
        self.tag = 'IF_%d' % NodeIfElse._num
        self.condition = condition
        self.iftrue = iftrue
        self.iffalse = iffalse
        
    def emit(self, local_variables, **kwargs):
        # Emit code for this scope's local variables (shouldn't be any)
        precode = super(NodeIfElse, self).emit()
        
        # Check condition
        precode.extend(self.condition.emit(local_variables, 1))

        # Jump around
        if self.iffalse is not None:
            precode.append(['<%s>' % self.tag, 'JZ', 'RB[1]', '<!%s>' % self.tag])
            precode.extend(self.iftrue.emit(local_variables, **kwargs))
            precode.append([None, 'JZ', 0, '</%s>' % self.tag])
            precode.append(['<!%s>' % self.tag, 'ARB', 0])
            precode.extend(self.iffalse.emit(local_variables, **kwargs))
            precode.append(['</%s>' % self.tag, 'ARB', 0])
        else:
            precode.append(['<%s>' % self.tag, 'JZ', 'RB[1]', '</%s>' % self.tag])
            precode.extend(self.iftrue.emit(local_variables, **kwargs))
            precode.append(['</%s>' % self.tag, 'ARB', 0])
        return precode


class NodeGoto:
    def __init__(self, location):
        self.location = location
    
    def emit(self, local_variables, **kwargs):
        return [['<GOTO>', 'JZ', 0, kwargs[self.location]]]


class NodeFor(NodeScope):
    _num = 0
    def __init__(self, condition, block, statement_1st=None, statement_every=None):
        super(NodeFor, self).__init__([block], [])
        NodeFor._num += 1
        self.tag = 'FOR_%d' % NodeFor._num
        self.condition = condition
        self.block = block
        self.statement_1st = statement_1st
        self.statement_every = statement_every
        
    def emit(self, local_variables, **kwargs):
        # Emit code for this scope's local variables (shouldn't be any)
        precode = super(NodeFor, self).emit()

        # 1st
        if self.statement_1st is not None:
            precode.extend(self.statement_1st.emit(local_variables))
        
        # Check condition
        precode.append(['<%s>' % self.tag, 'ARB', 0])
        precode.extend(self.condition.emit(local_variables, 1))
        precode.append([None, 'JZ', 'RB[1]', '</%s>' % self.tag])
        
        # Block
        kwargs['break_location'] ='</%s>' % self.tag
        precode.extend(self.block.emit(local_variables, **kwargs))

        # Post-iteration statement
        if self.statement_every is not None:
            precode.extend(self.statement_every.emit(local_variables))
        precode.append([None, 'JZ', 0, '<%s>' % self.tag])
        
        # Finish
        precode.append(['</%s>' % self.tag, 'ARB', 0])

        return precode


class NodeAssignment:
    def __init__(self, target, expression):
        self.target = target
        self.expression = expression
        # Assignment expression: trim last @-operand
        # (which must exist for a valid assignment)
        if self.target.postfix[-1] != '@':
            raise SyntaxError('Cannot assign to %s' % self.target.text)
        self.target.postfix = self.target.postfix[:-1]
    
    def emit(self, local_variables, **kwargs):
        precode = []
        precode.extend(self.target.emit(local_variables, 1))
        precode.extend(self.expression.emit(local_variables, 2))

        deref_tag = NodeExpression.unique_deref_tag()
        precode.append(['<%s>' % deref_tag, 'ADD', 0, 'RB[1]', '[</%s> + 3]' % deref_tag])
        precode.append(['</%s>' % deref_tag, 'ADD', 0, 'RB[2]', '[0]'])
        return precode


class NodeVariable:
    def __init__(self, name, array_size=None, is_global=False, array_init=None):
        self.name = name
        self.address = None
        self.array_size = array_size
        self.array_init = array_init
        self.is_global = is_global


class NodeCall:
    _num = 0
    def __init__(self, fname, parameters):
        NodeCall._num += 1
        self.call_id = 'CALL_%d' % NodeCall._num
        self.fname = fname
        self.parameters = parameters
        
    def emit(self, local_variables, **kwargs):
        precode = []

        # Special builtins (print() and scan())
        if self.fname == 'print':
            if len(self.parameters) != 1:
                raise SyntaxError('print() takes exactly 1 parameter')
            precode.extend(self.parameters[0].emit(local_variables, 1))
            precode.append(['<PRINT/>', 'OUT', 'RB[1]'])
            return precode
        elif self.fname == 'scan':
            if len(self.parameters) != 1:
                raise SyntaxError('scan() takes exactly 1 parameter')
            scan_call_id = 'SCAN_' + self.call_id[5:]
            precode.extend(self.parameters[0].emit(local_variables, 1))
            precode.append(['<%s>' % scan_call_id, 'ADD', 0, 'RB[1]', '[</%s> + 1]' % scan_call_id])
            precode.append(['</%s>' % scan_call_id, 'IN', '[0]'])
            return precode

        # Put return address on stack: 3 positions after the JZ-instruction below
        precode.append(['<%s>' % self.call_id, 'ADD', '</%s>' % self.call_id, 3, 'RB[1]'])

        # Put parameters (evaluate expressions as necessary) in RB[2], RB[3], ...
        for rbo, param in enumerate(self.parameters):
            precode.extend(param.emit(local_variables, rbo + 2))
        
        # Jump to designated location
        precode.append(['</%s>' % self.call_id, 'JZ', 0, '<FCN_%s>' % self.fname])

        return precode


class NodeExpression:
    _deref_num = 0
    def unique_deref_tag():
        NodeExpression._deref_num += 1
        return '@%d' % NodeExpression._deref_num

    def _infix_to_postfix(text):
        stk = deque()
        postfix = []
        precedence = {'==': 1, '<': 1, '>': 1, '<=': 1, '>=': 1, '+': 2, '-': 2, '*': 3, '&': 9, '@': 9}

        i = 0
        while i < len(text):
            if text[i].isspace():
                i += 1
            elif text[i].isalnum() or text[i] == '_':
                j = 1
                while i+j < len(text) and (text[i+j].isalnum() or text[i+j] == '_'):
                    j += 1
                
                symbol = text[i:(i+j)]
                postfix.append(symbol)
                if is_valid_name(symbol):
                    postfix.append('@')  # "At"-operator
                i += j
            elif text[i] == '&':
                stk.append('&')
                i += 1
            elif text[i] == '[':
                stk.append('[')
                i += 1
            elif text[i] == '(':
                stk.append('(')
                i += 1
            elif text[i] == ')':
                while len(stk) > 0 and stk[-1] != '(':
                    postfix.append(stk.pop())
                stk.pop() # Discard '('
                i += 1
            elif text[i] == ']':
                while len(stk) > 0 and stk[-1] != '[':
                    postfix.append(stk.pop())
                stk.pop()  # Discard '['
                postfix.append('+') # Dereference
                postfix.append('@')  # "At"-operator
                i += 1
            else:
                if i + 1 < len(text) and text[i:(i+2)] in precedence:
                    symbol = text[i:(i+2)]
                    i += 2
                else:
                    symbol = text[i]
                    i += 1
                while len(stk) > 0 and stk[-1] != '(' and stk[-1] != '[' and precedence[symbol] <= precedence[stk[-1]]:
                    if stk[-1] == '&' and postfix[-1] == '@':
                        postfix.pop()
                        stk.pop()
                    else:
                        postfix.append(stk.pop())
                stk.append(symbol)
        while len(stk) > 0:
            if stk[-1] == '&' and postfix[-1] == '@':
                postfix.pop()
                stk.pop()
            else:
                postfix.append(stk.pop())
        
        return postfix

    def __init__(self, text):
        self.text = text
        self.postfix = NodeExpression._infix_to_postfix(text)
    
    def emit(self, local_variables, rbo):
        precode = []
        rbo0 = rbo
        for item in self.postfix:
            if item == '==':  # Compare 2 top items in stack
                assert rbo > rbo0
                rbo -= 1
                precode.append(['<x==y>', 'EQ', 'RB[%d]' % (rbo - 1), 'RB[%d]' % rbo, 'RB[%d]' % (rbo - 1)])
            elif item == '<':  # ...
                assert rbo > rbo0
                rbo -= 1
                precode.append(['<x<y>', 'LT', 'RB[%d]' % (rbo - 1), 'RB[%d]' % rbo, 'RB[%d]' % (rbo - 1)])
            elif item == '>':  # ...
                assert rbo > rbo0
                rbo -= 1
                precode.append(['<x>y>', 'LT', 'RB[%d]' % rbo, 'RB[%d]' % (rbo - 1), 'RB[%d]' % (rbo - 1)])
            elif item == '<=':  # ...
                assert rbo > rbo0
                rbo -= 1
                precode.append(['<x<=y>', 'LT', 'RB[%d]' % rbo, 'RB[%d]' % (rbo - 1), 'RB[%d]' % (rbo - 1)])
                precode.append(['<x<=y>', 'MUL', -1, 'RB[%d]' % (rbo - 1), 'RB[%d]' % (rbo - 1)])
                precode.append(['<x<=y>', 'ADD',  1, 'RB[%d]' % (rbo - 1), 'RB[%d]' % (rbo - 1)])
            elif item == '>=':  # ...
                assert rbo > rbo0
                rbo -= 1
                precode.append(['<x<=y>', 'LT', 'RB[%d]' % (rbo - 1), 'RB[%d]' % rbo, 'RB[%d]' % (rbo - 1)])
                precode.append(['<x<=y>', 'MUL', -1, 'RB[%d]' % (rbo - 1), 'RB[%d]' % (rbo - 1)])
                precode.append(['<x<=y>', 'ADD',  1, 'RB[%d]' % (rbo - 1), 'RB[%d]' % (rbo - 1)])
            elif item == '+':  # Add 2 top items in stack
                assert rbo > rbo0
                rbo -= 1
                precode.append(['<x+y>', 'ADD', 'RB[%d]' % (rbo - 1), 'RB[%d]' % rbo, 'RB[%d]' % (rbo - 1)])
            elif item == '-' and rbo == rbo0 + 1:  # Invert sign
                precode.append(['<-x>', 'MUL', -1, 'RB[%d]' % (rbo - 1), 'RB[%d]' % (rbo - 1)])
            elif item == '-':  # Subtract 2 top items in stack
                assert rbo > rbo0
                rbo -= 1
                precode.append([None, 'MUL', -1, 'RB[%d]' % rbo, 'RB[%d]' % rbo])
                precode.append(['<x-y>', 'ADD', 'RB[%d]' % (rbo - 1), 'RB[%d]' % rbo, 'RB[%d]' % (rbo - 1)])
            elif item == '*':  # Multiplicate 2 top items in stack
                assert rbo > rbo0
                rbo -= 1
                precode.append(['<x*y>', 'MUL', 'RB[%d]' % (rbo - 1), 'RB[%d]' % rbo, 'RB[%d]' % (rbo - 1)])
            elif item == '@':  # Dereference top item in stack
                deref_tag = NodeExpression.unique_deref_tag()
                precode.append(['<%s>' % deref_tag, 'ADD', 0, 'RB[%d]' % (rbo - 1), '[</%s> + 2]' % deref_tag])
                precode.append(['</%s>' % deref_tag, 'ADD', 0, '[0]', 'RB[%d]' % (rbo - 1)])
            elif item.isnumeric():
                precode.append(['<%s/>' % item, 'ADD', 0, int(item), 'RB[%d]' % rbo])
                rbo += 1
            else:
                for v in local_variables[::-1]:
                    if v.name == item:
                        break
                else:
                    raise RuntimeError('Variable \'%s\' seems undefined' % item)
                
                if v.is_global:
                    precode.append([None, 'ADD', 0, v.address, 'RB[%d]' % rbo])
                    #precode.append([None, 'ADD', 'RB[0]', v.address, 'RB[%d]' % rbo])
                    rbo += 1
                else:
                    precode.append([None, 'ADD', 'RB[0]', v.address, 'RB[%d]' % rbo])
                    rbo += 1
        return precode


def is_valid_name(name):
    if not (name[0].isalpha() or name[0] == '_'):
        return False
    if not all([c.isalnum() or c == '_' for c in name]):
        return False
    return True


def is_empty_or_comment(text):
    return text.strip() == '' or text.lstrip().startswith('//')


def strip_ws_and_comments(text):
    comment = text.find('//')
    return text[:comment].strip() if comment >= 0 else text.strip()


def get_variable(text):
    text = text.strip()

    # Array type?
    left_bracket = text.rfind('[')
    right_bracket = text.rfind(']')
    if 0 < left_bracket and left_bracket < right_bracket:
        bracket_expression = text[(left_bracket + 1):right_bracket].strip()
        vname = text[:left_bracket].strip()
        array_type = True
    elif 0 < left_bracket and not left_bracket < right_bracket:
        raise SyntaxError('Missing \']\' after \'[\'')
    else:
        bracket_expression = ''
        vname = text.strip()
        array_type = False
    
    # Name?
    if not is_valid_name(vname):
        raise SyntaxError('Invalid variable-name \'%s\'' % vname)
    
    return vname, array_type, bracket_expression


def read_variable_definition(code, row, is_global=False):
    # -------------------------------------------
    # Parse a variable definition
    #
    # primitive:  int a
    #     array:  int b[10]
    # -------------------------------------------
    

    semicolon = code[row].find(';')
    if semicolon < 0 or not is_empty_or_comment(code[row][(semicolon + 1):]):
        raise SyntaxError('Invalid variable-definition', ('', row + 1, 0, code[row]))
    line = code[row][:semicolon].strip()
    if not line.startswith('int') or len(line) < 4  or line[4].isspace():
        raise SyntaxError('Only int-types allowed. (not \'%s\')' % line.split(' ')[0])
    vname, array_type, bracket_expression = get_variable(line[3:])

    if array_type:
        if not bracket_expression.isnumeric():
            raise SyntaxError('Invalid array-size (expected int-constant): \'%s\'' % bracket_expression, ('', row + 1, 0, code[row]))
        array_size = int(bracket_expression)
        if array_size <= 0:
            raise SyntaxError('Array-size must be positive, not \'%d\'' % array_size, ('', row + 1, 0, code[row]))
        
        right_bracket = code[row].find(']')
        equals = code[row].find('=')
        left_curly = code[row].find('{')
        right_curly = code[row].find('}')

        if right_bracket < equals and equals < left_curly and left_curly < right_curly and right_curly < semicolon:
            array_init = [int(x) for x in code[row][(left_curly + 1):right_curly].split(',')]
        elif equals < 0 and left_curly < 0 and right_curly < 0:
            array_init = None
        else:
            raise SyntaxError('Illegal array-initialization', ('', row + 1, 0, code[row]))
        print(array_init)
        return NodeVariable(vname, array_size, is_global, array_init), row + 1
    else:
        return NodeVariable(vname, None, is_global, None), row + 1


def read_forloop(code, row):
    # -------------------------------------------
    # Read for-loop block
    #
    # row --> for (assignment; condition; assignment) {
    #            ...
    #         }
    #         else <...>
    # -------------------------------------------
    forloop_line = strip_ws_and_comments(code[row])
    left_paren = forloop_line.find('(')
    right_paren = forloop_line.rfind(')')
    left_curly = forloop_line.rfind('{')
    semicolon1 = forloop_line.find(';')
    semicolon2 = forloop_line.rfind(';')
    if not (forloop_line.startswith('for') and 0 < left_paren and left_paren < semicolon1 and semicolon1 < semicolon2 and semicolon2 < right_paren and right_paren < left_curly):
        raise SyntaxError('Expected \'for (...; ...; ...) {\'', ('', row + 1, 0, code[row]))
    
    assignment1_text = forloop_line[(left_paren+1):semicolon1].strip()
    condition = NodeExpression(forloop_line[(semicolon1+1):semicolon2])
    assignment2_text = forloop_line[(semicolon2+1):right_paren].strip()
    should_be_empty_1 = forloop_line[(right_paren+1):left_curly].strip()
    should_be_empty_2 = forloop_line[(left_curly+1):].strip()

    if not (should_be_empty_1 == ''):
        raise SyntaxError('Unexpected \'%s\' in if-else-statement' % should_be_empty_1, ('', row + 1, 0, code[row]))
    if not (should_be_empty_2 == ''):
        raise SyntaxError('Unexpected \'%s\' in if-else-statement' % should_be_empty_2, ('', row + 1, 0, code[row]))
    
    statements = []
    for assignment_text in [assignment1_text, assignment2_text]:
        if assignment_text == '':
            statements.append(None)
        elif assignment_text.find('=') < 0:
            raise SyntaxError('Expected assignment, not \'%s\'' % assignment_text, ('', row + 1, 0, code[row]))
        else:
            target = NodeExpression(assignment_text[:assignment_text.find('=')].strip())
            expression = NodeExpression(assignment_text[(assignment_text.find('=') + 1):].strip())
            statements.append(NodeAssignment(target, expression))
    
    block, row = read_block(code, row + 1)
    
    return NodeFor(condition, block, statements[0], statements[1]), row


def read_ifelse(code, row):
    # -------------------------------------------
    # Read if-else block
    #
    # row --> if (condition) {
    #            ...
    #         }
    #         else <...>
    # -------------------------------------------
    if_line = code[row].strip()
    left_paren = if_line.find('(')
    right_paren = if_line.rfind(')')
    left_curly = if_line.rfind('{')
    if not ((if_line.startswith('if') or if_line.startswith('else if')) and 0 < left_paren and left_paren < right_paren and right_paren < left_curly):
        raise SyntaxError('Expected \'if (...) {\' or \'else if (...) {\'', ('', row + 1, 0, code[row]))
    
    condition = NodeExpression(if_line[(left_paren+1):right_paren])
    should_be_empty_1 = if_line[(right_paren+1):left_curly].strip()
    should_be_empty_2 = if_line[(left_curly+1):].strip()

    if not (should_be_empty_1 == ''):
        raise SyntaxError('Unexpected \'%s\' in if-else-statement' % should_be_empty_1, ('', row + 1, 0, code[row]))
    if not is_empty_or_comment(should_be_empty_2):
        raise SyntaxError('Unexpected \'%s\' in if-else-statement' % should_be_empty_2, ('', row + 1, 0, code[row]))

    if_block, row = read_block(code, row + 1)

    else_line = code[row].strip()
    if else_line.startswith('else if'):
        else_block, row = read_ifelse(code, row)
    elif else_line.startswith('else'):
        left_curly = else_line.rfind('{')
        should_be_empty_1 = else_line[4:left_curly].strip()
        should_be_empty_2 = else_line[(left_curly+1):].strip()
        if not (should_be_empty_1 == ''):
            raise SyntaxError('Unexpected \'%s\' in if-else-statement' % should_be_empty_1, ('', row + 1, 0, code[row]))
        if not is_empty_or_comment(should_be_empty_2):
            raise SyntaxError('Unexpected \'%s\' in if-else-statement' % should_be_empty_2, ('', row + 1, 0, code[row]))
        else_block, row = read_block(code, row + 1)
    else:
        else_block = None
    return NodeIfElse(condition, if_block, else_block), row


def read_block(code, row):
    # -------------------------------------------
    # Read a block in its entirety
    #
    #         function / if / while / ...  {
    # row -->   .
    #           .
    #           .
    #         }
    # -------------------------------------------
    local_variables = []
    statements = []
    while(row < len(code)):
        # Strip comments once and for all on this line
        line = strip_ws_and_comments(code[row])

        if is_empty_or_comment(line):
            row += 1
        elif line.startswith('int') and line[3].isspace():
            variable, row = read_variable_definition(code, row)
            local_variables.append(variable)
        elif line.startswith('if') and line[2:].lstrip().startswith('('):
            ifelse, row = read_ifelse(code, row)
            statements.append(ifelse)
        elif line.startswith('for') and line[3:].lstrip().startswith('('):
            forloop, row = read_forloop(code, row)
            statements.append(forloop)
        elif line.startswith('while') and line[5:].lstrip().startswith('('):
            warnings.warn('NYI')
            row = read_block(code, row+1)
        elif line.startswith('break;'):
            statements.append(NodeGoto('break_location'))
            row += 1
        elif line.startswith('return;'):
            statements.append(NodeGoto('return_location'))
            row += 1
        elif line == '}':
            #print('  %s' % ', '.join([variable[0] for variable in local_variables]))
            row += 1
            break
        elif 0 < line.find('(') and (line.find('=') == -1 or line.find('(') < line.find('=')):
            left_paren = line.find('(')
            right_paren = line.rfind(')')
            semicolon = line.find(';')
            if not (0 < left_paren and left_paren < right_paren and right_paren < semicolon):
                raise SyntaxError('Parenthesis \'()\' mis-match or missing \';\'', ('', row + 1, 0, code[row]))
            if not (is_valid_name(line[:left_paren]) and is_empty_or_comment(line[(right_paren + 1):semicolon]) and is_empty_or_comment(line[(semicolon + 1):])):
                raise SyntaxError('Failed to parse function', ('', row + 1, 0, code[row]))
            
            fname = line[:left_paren]
            args = [a.strip() for a in line[(left_paren + 1):right_paren].split(',')]
            statements.append(NodeCall(fname, [NodeExpression(a) for a in args]))
            row += 1
        elif 0 < line.find('='):
            semicolon = line.find(';')
            if semicolon < 0 or not is_empty_or_comment(line[(semicolon + 1):]):
                raise SyntaxError('Assignment not (properly) terminated with \';\'', ('', row + 1, 0, code[row]))
            
            target = NodeExpression(line[:line.find('=')].strip())
            expression = NodeExpression(line[(line.find('=') + 1):semicolon].strip())
            statements.append(NodeAssignment(target, expression))
            row += 1
        else:
            raise SyntaxError('Invalid expression', ('', row + 1, 0, code[row]))
    else:
        raise SyntaxError('Unexpected EOF', ('', row + 1, 0, 'EOF'))
    
    return NodeBlock(statements, local_variables), row


def read_function(code, row):
    # -------------------------------------------
    # Read function
    #
    # row --> void foo(int a, int b, int* result) {
    #            ...
    #         }
    # -------------------------------------------

    # Verify function structure
    left_paren = code[row].find('(')
    right_paren = code[row].rfind(')')
    left_curly = code[row].rfind('{')
    if not (code[row].startswith('void ') and 0 < left_paren and left_paren < right_paren and right_paren < left_curly):
        raise SyntaxError('Expected \'void <function-name>(...) {\'', ('', row + 1, 0, code[row]))
    
    # Read function name and definition
    fname = code[row][5:left_paren].strip()
    param_list = code[row][(left_paren+1):right_paren]
    should_be_empty_1 = code[row][(right_paren+1):left_curly].strip()
    should_be_empty_2 = code[row][(left_curly+1):].strip()
    if not is_valid_name(fname):
        raise SyntaxError('Invalid function-name \'%s\'' % fname, ('', row + 1, 0, code[row]))
    if not (should_be_empty_1 == ''):
        raise SyntaxError('Unexpected \'%s\' in function definition' % should_be_empty_1, ('', row + 1, 0, code[row]))
    if not is_empty_or_comment(should_be_empty_2):
        raise SyntaxError('Unexpected \'%s\' in function definition' % should_be_empty_2, ('', row + 1, 0, code[row]))

    # Read parameters
    param_defs = [param_def.strip() for param_def in param_list.split(',')]
    if param_defs[0] == '':
        param_defs.pop(0)
    if not all([param_def.startswith('int') and param_def[3].isspace() for param_def in param_defs]):
        raise SyntaxError('Only int-type is allowed for parameters', ('', row + 1, 0, code[row]))
    variables = [get_variable(param_def[3:]) for param_def in param_defs]
    if any([v[1] for v in variables]):
        raise SyntaxError('No array-types are allowed for parameters', ('', row + 1, 0, code[row]))
    params = [NodeVariable(v[0]) for v in variables]
    
    # Read function body
    block, row = read_block(code, row + 1)
    
    return NodeFunction(fname, params, block), row


def read_file(input_file):
    functions = []
    global_variables = []

    with open(input_file) as f:
        code = f.read().splitlines(keepends=False)
    
    try:
        row = 0
        while row < len(code):
            # Strip comments once and for all on this line
            line = strip_ws_and_comments(code[row])

            if is_empty_or_comment(line):
                row += 1
            elif line.startswith('int') and line[3].isspace():
                variable, row = read_variable_definition(code, row, is_global=True)
                global_variables.append(variable)
            elif line.startswith('void') and line[4].isspace():
                node_fcn, row = read_function(code, row)
                functions.append(node_fcn)
    except SyntaxError as e:
        print('\nERROR: %s, in %s:' % (e.msg, input_file))
        print('\n%5d: %s' % (e.lineno, e.text))
        sys.exit(1)
    return functions, global_variables


def assemble_precode_to_intcode(precode):
    intcode = []
    label_lookup = dict()
    labels = dict()

    opcodes = {
        'ADD': 1,
        'MUL': 2,
        'IN': 3,
        'OUT': 4,
        'JNZ': 5,
        'JZ': 6,
        'LT': 7,
        'EQ': 8,
        'ARB': 9,
        'STOP': 99
    }

    # PASS 1
    for line in precode:
        if line[0] is not None:
            label_lookup[line[0]] = len(intcode)
            labels[len(intcode)] = line[0]
        
        if line[1] not in opcodes:
            intcode.extend(line[1:])
            continue

        # Parameter modes
        assert line[1] in opcodes, 'Invalid op: %s' % line[1]
        intcode.append(opcodes[line[1]])
        parameter_mode = ''
        args = []
        for c in line[2:]:
            if isinstance(c, int):
                parameter_mode = '1' + parameter_mode  # Direct mode
                args.append(c)
            elif isinstance(c, str) and c.startswith('<'):
                assert c.endswith('>'), 'Invalid arg: %s' % c
                parameter_mode = '1' + parameter_mode  # Direct mode
                args.append(c)
            elif isinstance(c, str) and c.startswith('['):
                assert c.endswith(']'), 'Invalid arg: %s' % c
                parameter_mode = '0' + parameter_mode    # Relative mode
                args.append(c[1:-1])
            elif isinstance(c, str) and c.startswith('RB['):
                assert c.endswith(']'), 'Invalid arg: %s' % c
                parameter_mode = '2' + parameter_mode    # Relative mode
                args.append(c[3:-1])
            else:
                raise ValueError('%s not expected here' % c)
        intcode[-1] += 100*int(parameter_mode) if parameter_mode != '' else 0
        intcode.extend(args)
    
    # PASS 2
    for p in range(len(intcode)):
        c = intcode[p]
        if isinstance(c, str):
            if len(c.split()) == 3 and c.split()[1] in ['+', '-']:
                offset = int(c.split()[2]) if c.split()[1] == '+' else -int(c.split()[2])
                c = c.split()[0]
                intcode[p] = label_lookup.get(c, c) + offset
            else:
                intcode[p] = label_lookup.get(c, c)
        intcode[p] = int(intcode[p])
    
    return intcode, labels


if __name__ == '__main__':
    # > python intcode_cc.py -i divmod.c -o aout.txt && python intcode_vm.py aout.txt
    #sys.argv = ['intcode_cc.py', '-i', 'divmod.c']

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, nargs='+', required=True)
    parser.add_argument('-o', '--output', type=str, default=None)
    args = parser.parse_args()

    # Read code
    functions = []
    global_variables = []
    for input_file in args.input:
        _functions, _global_variables = read_file(input_file)
        functions.extend(_functions)
        global_variables.extend(_global_variables)
    
    program = NodeProgram(functions, global_variables)
    precode = program.emit()

    # Print what we got
    for line in precode:
        if line[0] is not None:
            print(('%30s : ' % line[0]) + str(line[1:]))
        else:
            print(('%30s : ' % '') + str(line[1:]))

    # --- LINK(?) ---
    intcode, labels = assemble_precode_to_intcode(precode)
    #for l, n in enumerate(intcode):
    #    print('%5d : %s' % (l, n))

    if args.output is not None:
        with open(args.output, 'w') as f:
            f.write(','.join(['%d' % c for c in intcode]))
    else:
        print('')
        print('------------------------------------ RUNNING ------------------------------------')
        machine = IntCode.Machine(intcode)
        machine.blocked = False

        max_steps = 10000
        while not machine.halted and max_steps > 0:
            instruction_length, disasm = machine.peek_forward()
            print("%20s %5d | %s" % (labels.get(machine.pos, ''), machine.pos, disasm))
            if machine.blocked:
                text = ''
                while len(text) == 0:
                    text = input('> ')
                machine.push_input(int(text))
                machine.blocked = False
            else:
                input()
            machine.step_forward()
            max_steps -= 1
        print('-------------------------------------- DONE -------------------------------------')
        for out in machine.pop_output():
            print(out)