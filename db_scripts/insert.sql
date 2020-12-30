insert into computer_configuration(CPU,GPU,RAM,MONITOR,MOUSE,KEYBOARD)
values('Intel Core i9','Nvidia GeForce RTX 3070','32 gb DDR4','Samsung 4K Curbat','Razer Naga','Razer X');
insert into rooms(NAME,NUMBER_OF_COMPUTERS,CONFIGURATION_TYPE_FK)
values('Gods Room','10',1);
insert into computers(room_fk,computer_cfg_id_pk)
values(1,1);
insert into computers(room_fk,computer_cfg_id_pk)
values(1,1);
insert into computers(room_fk,computer_cfg_id_pk)
values(1,1);
insert into computers(room_fk,computer_cfg_id_pk)
values(1,1);
insert into computers(room_fk,computer_cfg_id_pk)
values(1,1);
insert into computers(room_fk,computer_cfg_id_pk)
values(1,1);
insert into computers(room_fk,computer_cfg_id_pk)
values(1,1);
insert into computers(room_fk,computer_cfg_id_pk)
values(1,1);
insert into computers(room_fk,computer_cfg_id_pk)
values(1,1);
insert into computers(room_fk,computer_cfg_id_pk)
values(1,1);
insert 
into appointments(computer_id,client_id,appointment_date,start_time,end_time,price)
values(1,1,SYSDATE,TO_DATE('2020/12/31 09:30:00', 'yyyy/mm/dd hh24:mi:ss'),TO_DATE('2020/12/31 11:30:00', 'yyyy/mm/dd hh24:mi:ss'),6);
