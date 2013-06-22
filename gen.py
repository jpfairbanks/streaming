fp = open("data.txt", 'w')

data = [ str(i) + '\n' for i in range(100)]
fp.writelines(data)

fp.close()
