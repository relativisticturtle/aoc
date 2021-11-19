//
// python intcode_cc.py -i math.c memory.c sort.c ../2021/y2019_day01.c -o aout.txt && python intcode_vm.py aout.txt < ../2019/input01.txt
//


int input[100];
int divres[2];

void main() {
    int L;
    for(L=0; L<100; L=L+1) {
        scan(&input[L]);
    }

    // PART 1
    int fuel_requirement;
    fuel_requirement = 0;

    
    int a;
    for(a=0; a<L; a=a+1) {
        divmod(divres, input[a], 3);
        fuel_requirement = fuel_requirement + divres[0] - 2;
    }
    print(fuel_requirement);

    // PART 2
    fuel_requirement = 0;
    for(a=0; a<L; a=a+1) {
        int w;
        w = input[a];
        for(;1;) {
            divmod(divres, w, 3);
            w = divres[0] - 2;
            if(w <= 0) {
                break;
            }
            fuel_requirement = fuel_requirement + w;
        }
    }
    print(fuel_requirement);
}
