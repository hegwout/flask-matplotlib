# flask-matplotlib
A Flask Docker with matplotlib

### TODO
```sh
mv env.txt .env
```

### RUN
```
docker-compose up 
docker-compose exec python sh -c "flask sendmail"
```
OR
```sh
docker run -v /data/http/flask-matplotlib-docker:/www flask-matplotlib-docker_python sh -c "flask sendmail"
```
### DB

```sql
CREATE TABLE `fos_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(180)  NOT NULL,
  `username_canonical` varchar(180)  NOT NULL,
  `email` varchar(180)  NOT NULL,
  `email_canonical` varchar(180)  NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  `salt` varchar(255)  DEFAULT NULL,
  `password` varchar(255)  NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `confirmation_token` varchar(180)  DEFAULT NULL,
  `password_requested_at` datetime DEFAULT NULL,
  `roles` longtext  NOT NULL COMMENT '(DC2Type:array)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_957A647992FC23A8` (`username_canonical`),
  UNIQUE KEY `UNIQ_957A6479A0D96FBF` (`email_canonical`),
  UNIQUE KEY `UNIQ_957A6479C05FB297` (`confirmation_token`)
) ENGINE=InnoDB ;
```


### REF
https://github.com/rui/docker-matplotlib


###