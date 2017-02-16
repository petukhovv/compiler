# include <stdio.h>

int main () {
  int i = 0;
  int s = 0; 

  while (i < 100000) {
    int j = 0;

    while (j < 100000) {    
      s += j;
      j++;
    }

    s += i;
    i++;
  }

  printf ("%d\n", s);
  return 0;
}
