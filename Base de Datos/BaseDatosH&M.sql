CREATE DATABASE HYM;
USE HYM;

CREATE TABLE Categorias(
Id_cate int auto_increment primary key,
NombreCate varchar(50)
);

select * from Categorias;
CREATE TABLE Mujer(
Id_proM int auto_increment primary key,
Nombre varchar(80),
precioMu decimal(10,2),
Id_cate int,
foreign key (Id_cate) references Categorias(Id_cate)
);
select * from Mujer;
CREATE TABLE Bebe(
Id_ProBebe int auto_increment primary key,
NombreProBebe varchar(70),
Precio decimal(10,2),
Id_cate int,
foreign key (Id_cate) references Categorias(Id_cate)
);
select * from Bebe;
CREATE TABLE Hombre(
Id_ProHombre int auto_increment primary key,
NombreProHombre varchar(100),
PrecioHombre decimal(10,2),
Id_cate int,
foreign key (Id_cate) references Categorias(Id_cate)
);
select * from Hombre;
CREATE TABLE Niños(
Id_ProNiño int  auto_increment primary key,
NombreProNiño varchar(90),
PrecioNiños decimal(10,2),
Id_cate int,
foreign key (Id_cate) references Categorias(Id_cate)
);
drop table Niños;
CREATE TABLE Home(
Id_ProHome int auto_increment primary key,
NombreProHome varchar(90),
PrecioHome decimal(10,2),
Id_cate int,
foreign key (Id_cate) references Categorias(Id_cate)
);

CREATE TABLE Beauty(
Id_ProBeauty int auto_increment primary key,
NombreProBeauty varchar(90),
PrecioBeauty decimal(10,2),
Id_cate int,
foreign key (Id_cate) references Categorias(Id_cate)
);

CREATE TABLE Sport(
Id_ProSport int auto_increment primary key,
NombreProSport varchar(80),
PrecioSport decimal(10,2),
Id_cate int,
foreign key (Id_cate) references Categorias(Id_cate)
);

CREATE TABLE Productos(
Id_Productos int auto_increment primary key,
NombrePro varchar(60),
Precios decimal(10,2),
Id_cate int,
foreign key (Id_cate) references Categorias(Id_cate)
);

select * from Productos;

