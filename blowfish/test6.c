#include <stdio.h>
#include <string.h>

int badfunc(char *string1, char *string2) {

  char  buffer1[1024];
  char  buffer2[1024];


  printf("running badfunc");
  if(strlen(string1)>=sizeof(buffer1)) {
    printf("\n\t(!) 1 overflow detected.\n");
    printf("\t(-) exiting...\n\n");
    return -1;
  }
  else {
    printf("\n\t(+) copying string1 into the buffer...");
    snprintf(buffer1,sizeof(buffer1),"%s",string1);
    printf("\t\t[done] (%d)\n", strlen(buffer1));
  }

  if(strlen(string2)>=sizeof(buffer2)*3) {
    printf("\n\t(!) overflow detected.\n");
    printf("\t(-) exiting...\n\n");
    return -1;
  }
  else {
    printf("\t(+) copying string2 into the buffer...");
    printf("buffer1 * 3: %d", sizeof(buffer1)*3);
    snprintf(buffer2,sizeof(buffer1)*3,"%s",string2);
    printf("\t\t[done] (%d)\n\n", strlen(buffer2));
  }

  return 0;
}

int main(int argc, char *argv[]) {
	printf("%d", argc);
	//printf("%s\n--\n--%s\n--\n--%s\n--\n--%s\n--\n--", argv[1], argv[2], argv[3], argv[4]);
	if(argc != 3)
		return -1;
   	
	badfunc(argv[2], argv[1]);

  	return 0;
}


