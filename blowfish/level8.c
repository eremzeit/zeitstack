#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
	if(argc < 3)
		return -1;
	funct(argv, 0x0000000012345678, 0x069696969, 0x0fafafafa);
}

int funct(char **input, int a, int b, int c) {
  char  buffer[64];
  char  *pointer = "changeme";
  int x1, x2, x3, x4;
  x1 = 0;
  x2 = 0;


  //strncpy(buffer, input, sizeof(buffer-1));
	
  printf("\n\tsizeof buffer: %p", sizeof(buffer)-1);
  printf("\n\tpointer: ");
  printf(pointer);
  printf("\n\n");

  printf(input[2],0x69696969, &x1, &x2);
  printf("\n\nx1, %10x\tx2: %10x\n\n", x1, x2);

  printf("\n\tinput: ");
  printf(input[3]);
  printf("\n\n");


	//run some tests here
	/*
  	printf("%x%x%x%x\t%n%n%n%n%10x\n\n", 0x41424344, 0x70717273, 0x123475, 0x123476, &x1, &x2, &x3, &x4, 0x99999999);
	printf("%10p%10p%10p%10p", x1, x2, x3, x4);
  	//printf("%8x%8x%8x%8x", 0x0a0b0c0d, 0x70717273, 0x123475, 0x123476);
	*/
  return 0;
}

