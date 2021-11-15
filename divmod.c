//
int two_xp[32] = {1, 2, 4, 8, 16, 32, 64, 128, 256};

// C Lite
void divmod(int res, int a, int b) {
    int p;
    int xp2[32];
    xp2[0] = 1;
    for(p=1; p<32; p=p+1) {
        xp2[p] = 2*xp2[p-1];
        if(b*xp2[p] > a) {
            break;
        }
    }

    res[0] = 0;
    for(p=p-1; p>=0; p=p-1) {
        if(b*xp2[p] <= a) {
            res[0] = res[0] + xp2[p];
            a = a - b*xp2[p];
        }
    }
    res[1] = a;
}


void main() {
    int a;
    int b;
    int res[2];
    two_xp[9] = 512;
    print(two_xp[9]);

    scan(&a);
    scan(&b);
    divmod(res, a, b);

    print(res[0]);
    print(res[1]);
}


// --- The stack ---
// Stack pointer: RB
//   Top of stack: RB[0]
//   Push <X>: "ARB 1, ADD X, 0, RB[0]"
//   Pop     : "ARB -1, ADD RB[1], 0, ..."
//
// Variables: RB[-3], RB[-2], RB[-1]



// -------------------------------
//   109   &stack              : initialize RB

//   109    1                  : ...
// 21101   return_loc  0    0  : push return location on stack

//   109    1                  : ...
// 21101   param_1     0    0  : push parameter 1 on stack

//   109    1                  : ...
// 21101   param_2     0    0  : push parameter 2 on stack

//  1105      0    &main       : CALL main()

//    99                       : STOP


// main()
//   109   local_var_size      : setup stack frame for local vars


// At NodeCall:
//     RB[0]  --->  &RB_old
//     RB[1]  --->  return_loc
//     RB[2]  --->  param_1
//     RB[3]  --->  param_2
//     RB[4]  --->  ...

// At NodeFunction:
//     RB[-7] --->  &RB_old
//     RB[-6] --->  return_loc
//     RB[-5] --->  param_1
//     RB[-4] --->  param_2
//     RB[-3] --->  var_1
//     RB[-2] --->  var_2
//     RB[-1] --->  var_3
//     RB[0]  --->  &RB_new
//     RB[1]  --->  postfix calc stack, etc...

// RB-position only manipulated at NodeFunction

// At NodeExpression:
//     RB[offset] <--- results goes here


// At NodeAssignment:
//     RB[0] target address
//     RB[1] value to put in target
