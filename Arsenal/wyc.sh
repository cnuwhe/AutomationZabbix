#!/bin/bash
sudo ./nettop.stp > result.txt
awk -F ':' 'BEGIN {count=0;} {pid[count] = $1;recv[count]=$2;flag[count]=$3;count++;}; 
END{
flag2=0
for(i=0;i<NR;i++)
{
	if(flag[i]==1)
{
		half_count=i;
		break;
}
}
for (i = 0; i < half_count; i++)
{
	for(j=half_count;j<NR;j++)
{
		if(pid[i]==pid[j]&&recv[i]!=0&&recv[j]!=0&&recv[i]/recv[j]>5)
		{
			printf("%d\n",pid[i])
			
			flag2=1
			break
		}	
		
}
if(flag2==1)
break
} 
if(flag2==0)
{
	printf("%d\n",32767)
}
}' result.txt > result2.txt
awk '{print;}' result2.txt 
