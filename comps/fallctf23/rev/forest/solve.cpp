#include <iostream>
#include <map>
int factorial(int param) {
    if (param == 0) {
        return 1;
    }
    int blah = factorial(param - 1);
    return param * blah;
}

int combination(int param_1, int param_2, std::map<std::pair<int, int>, int> &memo) {
  if (memo.find(std::make_pair(param_1, param_2)) != memo.end()) {
    return memo[std::make_pair(param_1, param_2)];
  }
  int iVar1 = 0;
  int iVar2 = 0;
  
  if (param_2 != 0) {
    iVar2 = 1;
    if (param_2 != param_1) {
      iVar1 = combination(param_1 - 1,param_2 - 1, memo);
      iVar2 = combination(param_1 - 1,param_2, memo);
      iVar2 = iVar2 + iVar1;
    }
    memo[std::make_pair(param_1, param_2)] = iVar2;
    return iVar2;
  }
  return 1;
}

int main() {
    std::map<std::pair<int, int>, int> memo;
    for (int i = 0; i < 100; i++) {
        if (factorial(i) == -0x80000000) {
            for (int j = i; j < 100; j++) {
                // std::cout << i << " " << j << std::endl;
                if (combination(j, i, memo) == 0x1a93c4e2) {
                    std::cout << i << " " << j << std::endl;
                    return 0;
                }
            }

        }
    }
}

