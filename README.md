# Log Analysis Udacity Project
 An internal reporting tool that will use information from the database to discover what kind of articles the site's readers like and much more information.
#### Project Contents
     project.py
     newsdata.sql

### Queries:
* <h4>Popular Articles</h4>
```sql
select ar.title , count(*) as Total_Count from articles ar 
join log l on l.path like concat('%', ar.slug, '%') 
where l.status like '%200%'
group by ar.title, l.path 
order by Total_Count desc limit 3

```
* <h4>Popular Authors</h4>
```sql
select au.name,count(*) as Total_count from articles ar  
join log l on l.path like concat('%', ar.slug, '%') 
join authors au on au.id = ar.author 
where l.status like '%200%' group by au.name
order by Total_Count desc

```
* <h4>Error % based  on failed requests</h4>
```sql
select coalesce (to_char(date, 'MON DD,YYYY'),'') as date, coalesce (to_char(rate, '999D9'),'') as rate  
from (  with a as(select count(*)::decimal as error,date(time) from public.log 
where status like '404%'  
group by date(time) order by date(time)),b as 
(select count(*)::decimal as success,date(time) from public.log 
where status like '200%'  
group by date(time) order by date(time))select date, ((a.error/b.success) *100.0)::decimal as rate 
from a join b using(date)  ) as finalvalue where rate > 1.0



```

## How to Run
* <h4>Download and install <a href="https://www.vagrantup.com/">Vagrant</a> and <a href="https://www.virtualbox.org/wiki/Downloads">VirtualBox.</a></h4>
* <h4>Download the project zip file and extract it </h4>
* <h4>Copy the extracted folder to the downloaded  vagrant directory </h4>
* <h4>Open a terminal inside the vagrant directory and type `vagrant up`</h4>
* <h4>Once the download and installation completes type `vagrant ssh` in terminal</h4>
* <h4>Download the <a href="https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip">data</a></h4>
  You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant           directory, which is shared with your virtual machine.
* <h4>Load the data into the database</h4>
    Type it in the terminal
  <pre>psql -d news -f newsdata.sql;</pre>
* <h4>Run code</h4>
  <pre>python project.py</pre>
  
### 

