#include<stdio.h>

float func(int j, float g) {
    return g*j;
}

int main()
{
  int i = 258;
  float f = 3.141592653589793;
  float h = func(i,f);
  printf("%3.4f", h);
  return 0;
}
