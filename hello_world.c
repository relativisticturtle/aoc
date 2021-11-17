void main() {
    int a;
    int b;
    int res[2];
    
    scan(&a);
    scan(&b);
    divmod(res, a, b);

    print(res[0]);
    print(res[1]);

    int test[10];
    memcpy(test, _xp2, 10);
    for(a=0; a<10; a=a+1) {
        print(test[a]);
    }
}
