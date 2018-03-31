#requires ongoing_industry.txt and ongoing_startup_name.txt
ind = open('ongoing_industry.txt', 'r')
name = open('ongoing_startup_name.txt', 'r')
file = open('ongoing_industries_list.txt', 'w')

Industries = dict() #dict of ico grouped by industries

#group ico
for line1, line2 in zip(ind, name):
    line1 = line1.rstrip()
    line2 = line2.rstrip()
    ind_list = list(map(str, line1.split(', ')))
    for i in range (len(ind_list)):
        if ind_list[i] in Industries:
            Industries[ind_list[i]].append(line2)
        else:
            Industries[ind_list[i]] = [line2]

#print groups
for indust in Industries:
    file.write(indust + ': ')
    file.write(" ".join(Industries[indust]) + '\n')

file.close()
ind.close()
name.close()
