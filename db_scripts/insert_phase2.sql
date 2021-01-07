-- because clients can't be introduced by hand in the database due to the hash of the password while registering
-- they're "introduced" in the database with a script in python
-- therefore, these updates are made to give the data credibility (and sense)

update clients set account_credits = 55, registration_date = TO_DATE('2020/12/25 11:22:33', 'YYYY/MM/DD hh24:MI:SS') where user_id_pk=1;
update clients set account_credits = 20, registration_date = TO_DATE('2020/12/25 15:46:12', 'YYYY/MM/DD hh24:MI:SS') where user_id_pk=2;
update clients set account_credits = 10, registration_date = TO_DATE('2020/12/26 13:29:59', 'YYYY/MM/DD hh24:MI:SS') where user_id_pk=3;
update clients set account_credits = 15, registration_date = TO_DATE('2020/12/26 14:01:05', 'YYYY/MM/DD hh24:MI:SS') where user_id_pk=4;
update clients set account_credits = 40, registration_date = TO_DATE('2020/12/25 23:44:41', 'YYYY/MM/DD hh24:MI:SS') where user_id_pk=5;

insert into appointments(computer_id,client_id,appointment_date,start_time,end_time,price,employee_id_pk)
values(1,1,TO_DATE('2020/12/31 07:00:00', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/31 09:00:00', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/31 11:00:00', 'YYYY/MM/DD hh24:MI:SS'),8.75,4);
insert into appointments(computer_id,client_id,appointment_date,start_time,end_time,price,employee_id_pk)
values(1,1,TO_DATE('2020/12/30 07:00:00', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/30 09:00:00', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/30 11:00:00', 'YYYY/MM/DD hh24:MI:SS'),8.75,4);
insert into appointments(computer_id,client_id,appointment_date,start_time,end_time,price,employee_id_pk)
values(1,1,TO_DATE('2020/12/30 07:00:00', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/30 19:00:00', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/30 21:00:00', 'YYYY/MM/DD hh24:MI:SS'),8.75,4);
insert into appointments(computer_id,client_id,appointment_date,start_time,end_time,price,employee_id_pk)
values(1,1,TO_DATE('2020/12/31 07:00:00', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/31 19:00:00', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/31 21:00:00', 'YYYY/MM/DD hh24:MI:SS'),8.75,4);
insert into appointments(computer_id,client_id,appointment_date,start_time,end_time,price,employee_id_pk)
values(2,3,TO_DATE('2020/12/26 07:00:00', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/26 11:00:00', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/26 13:00:00', 'YYYY/MM/DD hh24:MI:SS'),8.75,4);
insert into appointments(computer_id,client_id,appointment_date,start_time,end_time,price,employee_id_pk)
values(16,2,TO_DATE('2020/12/26 07:00:00', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/26 11:00:00', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/26 13:00:00', 'YYYY/MM/DD hh24:MI:SS'),8.75,4);
insert into appointments(computer_id,client_id,appointment_date,start_time,end_time,price,employee_id_pk)
values(16,2,TO_DATE('2020/12/28 09:00:00', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/28 12:00:00', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/28 14:00:00', 'YYYY/MM/DD hh24:MI:SS'),8.75,4);
insert into appointments(computer_id,client_id,appointment_date,start_time,end_time,price,employee_id_pk)
values(7,1,TO_DATE('2020/12/28 08:52:16', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/28 13:00:00', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/28 16:00:00', 'YYYY/MM/DD hh24:MI:SS'),10.5,4);
insert into appointments(computer_id,client_id,appointment_date,start_time,end_time,price,employee_id_pk)
values(7,4,TO_DATE('2020/12/28 08:52:16', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/28 16:00:00', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/12/28 19:00:00', 'YYYY/MM/DD hh24:MI:SS'),10.5,4);
insert into appointments(computer_id,client_id,appointment_date,start_time,end_time,price,employee_id_pk)
values(36,5,TO_DATE('2020/01/01 08:52:16', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/01/01 09:00:00', 'YYYY/MM/DD hh24:MI:SS'),TO_DATE('2020/01/01 17:00:00', 'YYYY/MM/DD hh24:MI:SS'),22,4);

insert into feedbacks(client_fk, message, feedback_date)
values(1,'Great place to play some games with your budddies.',TO_DATE('2020/12/31 16:33:41', 'YYYY/MM/DD hh24:MI:SS'));
insert into feedbacks(client_fk, message, feedback_date)
values(2,'Cheap prices, great computers, clean rooms. OK!',TO_DATE('2020/12/30 12:25:16', 'YYYY/MM/DD hh24:MI:SS'));
insert into feedbacks(client_fk, message, feedback_date)
values(3,'Superb atmosphere. Computers are highly capable, staff is friendly and prices are low. 10/10',TO_DATE('2020/12/30 09:07:55', 'YYYY/MM/DD hh24:MI:SS'));
insert into feedbacks(client_fk, message, feedback_date)
values(4,'Gaming is ok at them, but what I love the most is the site.',TO_DATE('2021/01/03 13:16:11', 'YYYY/MM/DD hh24:MI:SS'));
insert into feedbacks(client_fk, message, feedback_date)
values(5,'It`s ok if you`ve got time to lose.',TO_DATE('2021/01/05 12:15:02', 'YYYY/MM/DD hh24:MI:SS'));

commit work;