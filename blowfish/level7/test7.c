int main(int argc, char *argv[]) {
 
  int i;
  char  buffer[32];
//char  *key1 = "/";
  char  *p1, *p2, *p3, *p4, *p5;
  char  key2[2], key3[2], key4[2], key5[2];
 
//  if(argc != 2)
//    return -1;
 
  for(i = 1; i < argc; i++) {
        memset(argv[i], 0, strlen(argv[i]));
  }
  sprintf(key2, "%c", 0x90); // nop
  sprintf(key3, "%c", 0xeb); // jmp
  sprintf(key4, "%c", 0xcd); // int
  sprintf(key5, "%c", 0xff); // still easy
 
//p1 = strstr(argv[0], key1);
  p2 = strstr(argv[0], key2);
  p3 = strstr(argv[0], key3);
  p4 = strstr(argv[0], key4);
  p5 = strstr(argv[0], key5);
 
  if (p2 != 0 || p3 != 0 || p4 != 0 || p5 != 0) {
    printf("Access denied.\n");
    return -1;
  }
  else {
    printf("Access granted.\n");
  }
 
  strcpy(buffer, argv[0]);
  printf("argv[0]: %s", argv[0]);

  return 0;
}

