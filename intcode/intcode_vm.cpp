// "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64"
// cl /EHsc intcode_vm.cpp

#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <iostream>
#include <fstream>


#define MAX_SIZE 100000000
int64_t code[MAX_SIZE];


int64_t eval(int64_t p, int mode, int64_t rb) {
    if(mode == 0) {
        if(p >= 0 && p <= MAX_SIZE)
            return code[p];
        std::cout << "Illegal access: code[" << p << "]" << std::endl;
        exit(EXIT_FAILURE);
    }
    else if(mode == 1) {
        return p;
    }
    else if(mode == 2) {
        if(rb + p >= 0 && rb + p <= MAX_SIZE)
            return code[rb + p];
        std::cout << "Illegal access: code[" << rb << "+" << p << "]" << std::endl;
        exit(EXIT_FAILURE);
    }
    std::cout << "Illegal mode for eval: " << mode << std::endl;
    exit(EXIT_FAILURE);
}

void assign(int64_t val, int64_t p, int mode, int64_t rb) {
    if(mode == 0) {
        if(p >= 0 && p <= MAX_SIZE) {
            code[p] = val;
            return;
        }
        std::cout << "Illegal access: code[" << p << "]" << std::endl;
        exit(EXIT_FAILURE);
    }
    else if(mode == 1) {
        std::cout << "Immediate mode forbidden for assignment" << std::endl;
        exit(EXIT_FAILURE);
    }
    else if(mode == 2) {
        if(rb + p >= 0 && rb + p <= MAX_SIZE) {
            code[rb + p] = val;
            return;
        }
        std::cout << "Illegal access: code[" << rb << "+" << p << "]" << std::endl;
        exit(EXIT_FAILURE);
    }
    std::cout << "Illegal mode for assign: " << mode << std::endl;
    exit(EXIT_FAILURE);
}


int64_t run() {
    int64_t n = 0;
    int64_t i = 0;
    int64_t rb = 0;
    bool stop = false;

    while(!stop) {
        if(i<0 || i>=MAX_SIZE) {
            std::cout << "Illegal instruction-address" << i << std::endl;
            exit(EXIT_FAILURE);
        }

        int OP = code[i] % 100;
        int A = (code[i] / 10000) % 10;
        int B = (code[i] / 1000) % 10;
        int C = (code[i] / 100) % 10;
        
        //std::cout << "[" << i << "] " << code[i] << " : " << code[i + 1] << ", " << code[i + 2] << ", " << code[i + 3] << std::endl;

        switch(OP) {
        case 1:
            assign(eval(code[i+1], C, rb) + eval(code[i+2], B, rb), code[i+3], A, rb);
            i += 4;
            break;
        case 2:
            assign(eval(code[i+1], C, rb) * eval(code[i+2], B, rb), code[i+3], A, rb);
            i += 4;
            break;
        case 3:
            int64_t x;
            std::cin >> x;
            assign(x, code[i+1], C, rb);
            i += 2;
            break;
        case 4:
            std::cout << eval(code[i+1], C, rb) << std::endl;
            i += 2;
            break;
        case 5:
            if(eval(code[i+1], C, rb) != 0)
                i = eval(code[i+2], B, rb);
            else
                i += 3;
            break;
        case 6:
            if(eval(code[i+1], C, rb) == 0)
                i = eval(code[i+2], B, rb);
            else
                i += 3;
            break;
        case 7:
            assign(eval(code[i+1], C, rb) < eval(code[i+2], B, rb) ? 1 : 0, code[i+3], A, rb);
            i += 4;
            break;
        case 8:
            assign(eval(code[i+1], C, rb) == eval(code[i+2], B, rb) ? 1 : 0, code[i+3], A, rb);
            i += 4;
            break;
        case 9:
            rb += eval(code[i+1], C, rb);
            i += 2;
            break;
        case 99:
            stop = true;
            break;
        default:
            std::cout << "Invalid OP: " << OP << std::endl;
            exit(EXIT_FAILURE);
        }
        n++;
    }
    return n;
}


int main(int argc, const char* argv[]) {
    if(argc < 2) {
        std::cout << "Usage: " << argv[0] << " intcode_file.txt" << std::endl;
        exit(EXIT_FAILURE);
    }

    std::memset(code, 0, sizeof code);
    std::ifstream infile(argv[1]);
    int i;
    for(i=0; i<MAX_SIZE && !infile.eof();) {
        infile >> code[i++];
        if (infile.peek() == ',')
            infile.ignore();
    }
    std::cout << i << " integers read" << std::endl;

    //code[1] = 76;
    //code[2] = 21;

    int64_t n = run();
    std::cout << "done! " << n << " instructions executed." << std::endl;
    //std::cout << code[0] << std::endl;
}