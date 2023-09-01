nums = [16, 9, 3, 15, 3, 20, 6, 20, 8, 5, 14, 21, 13, 2, 5, 18, 19, 13, 1, 19, 15, 14]
flag = ''
for i in range(len(nums)):
    flag+=chr(nums[i]+64)
    if i == 6: flag+='{'
    if i == len(nums)-1: flag+='}'

print(flag)



