//
// python intcode_cc.py -i test.c -o aout.txt && intcode_vm aout.txt
//

int msg[] = "Hello world!";

int _buffer[20];
void prints(int s) {
    for(; s[0]; s+=1) {
        print(s[0]);
    }
}
void printd(int d) {
    if(d == 0) {
        print(48);
        return;
    }
    if(d < 0) {
        print(45);
        d = -d;
    }

    // buffer ptr - start from end
    int b;
    b = &_buffer[19];
    b[0] = 0;

    // div-by-10 loop
    int res[2];
    for(; d>0;) {
        b -= 1;
        divmod(res, d, 10);
        d = res[0];
        b[0] = 48 + res[1];
    }

    prints(b);
}
void printlf() {
    print(10);
}
void scans(int target, int i_max, int delim, int i_read) {
    int i;

    for(i=0; i<i_max;) {
        int c;
        scan(&c);
        if((c <= 0) + (c == delim)) {
            break;
        }
        if((delim == 10) * (c == 13)) {
            continue;
        }
        target[i] = c;
        i += 1;
    }
    target[i] = 0;
    i_read[0] = i;
}
void str2int(int s, int out) {
    for(; (s[0] == 32) + (s[0] == 9) + (s[0] == 10) + (s[0] == 13); s += 1) {
        // Skip whitespace characters
    }
    int sign;
    if(s[0] == 45) {
        sign = -1;
        s += 1;
    }
    else if(s[0] == 43) {
        sign = 1;
        s += 1;
    }
    else {
        sign = 1;
    }
    out[0] = 0;
    for(; (48 <= s[0]) * (s[0] <= 57); s+=1) {
        out[0] = 10*out[0] + s[0] - 48;
    }
}

void main() {
    int buffer[20];
    prints(msg);
    printlf();

    int i;
    int i_read;
    for(i=0; i<5; i=i+1) {
        scans(buffer, 19, 10, &i_read);
        prints(buffer);
        printlf();
    }
}