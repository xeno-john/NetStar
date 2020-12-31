insert into ic_employees(first_name,last_name,role,e_mail,phone_number,salary,hiring_date)
values('Ionut','Baltariu','Manager','saltyjohn31@gmail.com','0743783791',8000,TO_DATE('2018/10/01 09:00:00', 'YYYY/MM/DD HH:MI:SS'));
insert into ic_employees(first_name,last_name,role,e_mail,phone_number,salary,hiring_date)
values('Vlad','Paraschiv','Manager','vladparaschiv@gmail.com','0756718341',8000,TO_DATE('2018/10/01 09:00:00', 'YYYY/MM/DD HH:MI:SS'));
insert into ic_employees(first_name,last_name,role,e_mail,phone_number,salary,hiring_date)
values('Bejenariu','Razvan','Database Operator','razvanbeje1@gmail.com','0749351369',4800,TO_DATE('2018/10/01 09:00:00', 'YYYY/MM/DD HH:MI:SS'));
insert into ic_employees(first_name,last_name,role,e_mail,phone_number,salary,hiring_date)
values('Balta','Gabriel','Web - Back End','baltagaby@yahoo.com','0763493551',5120,TO_DATE('2018/10/01 09:00:00', 'YYYY/MM/DD HH:MI:SS'));
insert into ic_employees(first_name,last_name,role,e_mail,phone_number,salary,hiring_date)
values('Florin','Citu','Operator PC','citufl@yahoo.com','0755828239',3800,TO_DATE('2018/10/01 09:00:00', 'YYYY/MM/DD HH:MI:SS'));
insert into ic_employees(first_name,last_name,role,e_mail,phone_number,salary,hiring_date)
values('Ludovic','Bogdan','Operator PC','ludovic_bogdan@outlook.com','0756913512',3500,TO_DATE('2019/02/14 09:00:00', 'YYYY/MM/DD HH:MI:SS'));
insert into ic_employees(first_name,last_name,role,e_mail,phone_number,salary,hiring_date)
values('Rares','Orban','Operator PC','r.orban@yahoo.com','0743915290',3500,TO_DATE('2019/02/14 09:00:00', 'YYYY/MM/DD HH:MI:SS'));
insert into ic_employees(first_name,last_name,role,e_mail,phone_number,salary,hiring_date)
values('Luciano','Bote','Operator PC','luci.bote@gmail.com','0733793615',3300,TO_DATE('2020/03/15 09:00:00', 'YYYY/MM/DD HH:MI:SS'));
insert into ic_employees(first_name,last_name,role,e_mail,phone_number,salary,hiring_date)
values('Raluca','Tzurcan','Operator PC','tz.raluca@outlook.com','0756679812',3300,TO_DATE('2020/03/15 09:00:00', 'YYYY/MM/DD HH:MI:SS'));


insert into computer_configuration(CPU,GPU,RAM,MONITOR,MOUSE,KEYBOARD)
values('Intel Core i9','Nvidia GeForce RTX 3080 Ti','32 Gb DDR4 3200 MHz','Monitor LED Samsung 28" Curbat','Razer Naga Pro 3','Razer Huntsman');
insert into computer_configuration(CPU,GPU,RAM,MONITOR,MOUSE,KEYBOARD)
values('Amd Ryzen 5 3600','Nvidia GeForce RTX 2080 Ti','16 Gb DDR4 2666 MHz','Monitor LED Samsung 25" 1080p','Wireless Razer Mamba','Razer Black Widow');
insert into computer_configuration(CPU,GPU,RAM,MONITOR,MOUSE,KEYBOARD)
values('Amd Ryzen 5 2600X','Nvidia GeForce RTX 2060','16 Gb DDR4 2400 MHz','Monitor LED Samsung 25" 1080p','Logitech G502','Redragon K552B');

insert into rooms(NAME,NUMBER_OF_COMPUTERS,CONFIGURATION_TYPE_FK)
values('Gods Room','10',1);
insert into rooms(NAME,NUMBER_OF_COMPUTERS,CONFIGURATION_TYPE_FK)
values('Gladiators Room','12',2);
insert into rooms(NAME,NUMBER_OF_COMPUTERS,CONFIGURATION_TYPE_FK)
values('Pirates Room','15',3);

insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gods Room'),1);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gods Room'),1);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gods Room'),1);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gods Room'),1);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gods Room'),1);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gods Room'),1);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gods Room'),1);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gods Room'),1);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gods Room'),1);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gods Room'),1);

insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gladiators Room'),2);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gladiators Room'),2);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gladiators Room'),2);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gladiators Room'),2);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gladiators Room'),2);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gladiators Room'),2);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gladiators Room'),2);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gladiators Room'),2);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gladiators Room'),2);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gladiators Room'),2);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gladiators Room'),2);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Gladiators Room'),2);

insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Pirates Room'),3);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Pirates Room'),3);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Pirates Room'),3);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Pirates Room'),3);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Pirates Room'),3);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Pirates Room'),3);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Pirates Room'),3);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Pirates Room'),3);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Pirates Room'),3);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Pirates Room'),3);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Pirates Room'),3);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Pirates Room'),3);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Pirates Room'),3);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Pirates Room'),3);
insert into computers(room_fk,computer_cfg_id_pk)
values((select room_id_pk from rooms where name='Pirates Room'),3);

commit work;
