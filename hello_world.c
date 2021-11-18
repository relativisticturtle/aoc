int test[10] = {77, 76, 1, 43, 78, 32, 65, 2, 72, 16};

void main() {
    int a;
    int b;
    int res[2];
    
    //scan(&a);
    //scan(&b);
    //divmod(res, a, b);

    //print(res[0]);
    //print(res[1]);

    //int test[10];
    //memcpy(test, _xp2, 10);
    for(a=0; a<10; a=a+1) {
        print(test[a]);
    }
    print(-9999);
    int buffer[10];
    b = 10;
    
    //merge_into(test, buffer, 1, 2);
    sort_inplace(test, buffer, b);
    for(a=0; a<b; a=a+1) {
        print(test[a]);
    }
}
