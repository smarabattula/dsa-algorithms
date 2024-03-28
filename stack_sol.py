file_path = './test_file.txt'

# Read the file and extract the last column
data = []
with open(file_path, 'r') as file:
    for line in file:
        columns = line.strip().split('\t')
        data.append(columns[-1])

stack = []

i = 0
count = 0
for j in data[i]:
    if(ord(j) == 32):
        count += 1

stack.append((count,data[i]))
i += 1

while stack and i<len(data):
    count = 0
    for j in data[i]:
        if(ord(j) == 32):
            count += 1
    k = i
    while(count <= stack[-1][0]):
        print(1,stack)
        if(count < stack[-1][0]):
            stack.pop()

    print(stack)
    print(count,data[i])
    i += 1
    if i == 5:
        break



