def largest_consecutive_sum(nums, n):
    if n > len(nums):
        return None
    
    max_sum = float('-inf')
    current_sum = 0
    
    for i in range(len(nums)):
        if i >= n:
            current_sum -= nums[i - n]
        current_sum += nums[i]
        
        if current_sum > max_sum and i >= n - 1:
            max_sum = current_sum
    
    return max_sum

def largest_consecutive_sum2(numbers, n):
    
    max_sum = -999999999
    current_sum = 0
    
    for i in range(len(numbers)) : 
        current_sum = numbers[i+n]


nums = [20,4,5,7,9,11,12]
n = 2



#print(largest_consecutive_sum(nums,n))

print(largest_consecutive_sum(nums,n))

