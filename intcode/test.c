//
// python intcode_cc.py -i test.c -o aout.txt && intcode_vm aout.txt
//

int msg[13] = "Hello world!";


void prints(int s) {
    for(; s[0]; s+=1) {
        print(s[0]);
    }
}
void println() {
    print(10);
}

void main() {
    prints(msg);
    println();

    int i;
    for(i=0; i<101; i=i+1) {
        int x;
        scan(&x);
        print(x);
    }
}
