with
    Employees as (
        -- generating sample employee data
        select
            row_number() over () as Employee_id,
            case
                when Employee_id = 1 then 'Henry Peh'
                when Employee_id = 2 then 'Alice Tan'
                when Employee_id = 3 then 'Betty Ng'
                when Employee_id = 4 then 'Carol Wong'
                else 'David Lee'
                end as Name,
            dateadd(day, 200 * Employee_id, '2022-01-01')::date as Date_of_hire
        from (select 1 union all select 2 union all select 3 union all select 4 union all select 5) as t),
    Departments as (
        -- assigning departments to employees
        select
            e.Employee_id,
            case
                when e.Employee_id = 1 then 'Finance'
                when e.Employee_id = 2 then 'HR'
                when e.Employee_id = 3 then 'IT'
                when e.Employee_id = 4 then 'Marketing'
                else 'Operations'
                end as Department
        from Employees e),
    Courses as (
        -- generating sample course records for employees
        select
            e.Name as Employee_name,
            Course_name,
            least(
                    dateadd(
                            month, 6 * Employee_id * row_number() over (partition by Employee_id),
                            '2011-01-01'
                    ), '2023-06-01'
            )::date as Course_taken_date,
            concat(substring(Course_taken_date, 3, 2), 'SEM2') as Semester,
            case
                when floor(Employee_id / row_number() over (partition by Employee_id)) = 0 then 'A'
                when floor(Employee_id / row_number() over (partition by Employee_id)) = 1 then 'B'
                when floor(Employee_id / row_number() over (partition by Employee_id)) = 2 then 'C'
                when floor(Employee_id / row_number() over (partition by Employee_id)) = 3 then 'D'
                else 'E'
                end as Grade
        from Employees e
                 cross join (select
                                 'Math101' as course_name
                             union
                             select
                                 'Math202' as course_name
                             union
                             select
                                 'Physics101' as course_name
                             union
                             select
                                 'Physics202' as course_name
                             union
                             select
                                 'History303' as course_name
                             union
                             select
                                 'Chemistry404' as course_name
                             union
                             select
                                 'English505' as course_name
                             union
                             select
                                 'English606' as course_name) as c),
    -- Joining the three tables and calculating GPA
    base_joined as (select *,
                           case
                               when Grade = 'A' then 5
                               when Grade = 'B' then 4
                               when Grade = 'C' then 3
                               when Grade = 'D' then 2
                               when Grade = 'E' then 1
                               end as grade_point,
                           avg(grade_point) over (partition by Employee_id) as GPA
                    from Employees e
                             join Departments d using (Employee_id)
                             join Courses c on e.Name = c.Employee_name),
    -- Helper table to indicate whether an employee received at least one A in a certain year
    base_yearly_grade as (select
                              Employee_id,
                              left(Course_taken_date, 4)::int as course_taken_year,
                              least(
                                      sum(case when Grade = 'A' then 1 else 0 end), -- Marks if at least one course has an A
                                      1
                              ) as get_yearly_A -- 1 if the employee got at least one A in that year
                          from base_joined
                          group by 1, 2
                          order by 1, 2)
        ,
    -- Helper table to calculate how many times an employee got at least one A in the past 3 years
    base_consecutive_grade as (select
                                   Employee_id,
                                   course_taken_year,
                                   get_yearly_A,
                                   sum(get_yearly_A)
                                   over (partition by Employee_id order by course_taken_year rows between 2 preceding and current row) as cumulative_A
                               from base_yearly_grade
                               order by 1, 2)
-- Final selection of employees
select distinct
    Name
from base_joined
where left(Date_of_hire, 4)::int >= 2024      -- Filter new employees (hired in 2024)
  and Employee_id in (select distinct
                          Employee_id
                      from base_consecutive_grade
                      where cumulative_A > 0) -- Filter employees who got at least one A in class for 3 or more consecutive years during their study
order by GPA desc -- Rank employees by GPA (Grade Point Average) from the highest to lowest