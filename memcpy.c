//---------------------------------------------------
//
//  memcpy(*destination, *source)
//
//---------------------------------------------------

void memcpy(int destination, int source, int size) {
    int p;
    for(p=0; p<size; p=p+1) {
        destination[p] = source[p];
    }
}