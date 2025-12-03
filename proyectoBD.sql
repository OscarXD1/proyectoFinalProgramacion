-- create database proyectoBD;
-- use proyectoBD;

-- **********************
-- Tablas para direccion
-- **********************

create table municipio
(
idMunicipio int auto_increment primary key,
nombre varchar (255)
);

create table tipo_vialidad
(
idTipoVialidad int auto_increment primary key,
descripcion varchar (255)
);

create table colonia
(
idColonia int auto_increment primary key,
nombre varchar(255)
);

create table direccion
(
idDireccion int auto_increment primary key,
idMunicipio int,
idTipoVialidad int,
idColonia int,
calle varchar(255),

foreign key (idMunicipio) references municipio(idMunicipio),
foreign key (idTipoVialidad) references tipo_vialidad(idTipoVialidad),
foreign key (idColonia) references colonia(idColonia)
);

-- ***************************
-- tablas para crear sucursal
-- ***************************

create table tipo_farmacia
(
idTipoFarmacia int auto_increment primary key,
descripcion varchar (255)
);

create table farmacia
(
idFarmacia int auto_increment primary key,
nombre varchar (255)
);

create table clase_actividad
(
idClaseActividad int auto_increment primary key,
descripcion varchar (255)
);

create table cantidad_trabajadores
(
idCantidadTrabajadores int auto_increment primary key,
descripcion varchar (255)
);

-- TABLA CENTRAL SUCURSAL
create table sucursal
(
idSucursal int auto_increment primary key,
consultorio boolean default 0,
idFarmacia int,
idClaseActividad int,
idCantidadTrabajadores int,
idTipoFarmacia int, 
longitud decimal (12,8),
latitud decimal (12,8),
idDireccion int,

foreign key (idFarmacia) references farmacia(idFarmacia),
foreign key (idClaseActividad) references clase_actividad(idClaseActividad),
foreign key (idCantidadTrabajadores) references cantidad_trabajadores(idCantidadTrabajadores),
foreign key (idTipoFarmacia) references tipo_farmacia(idTipoFarmacia),
foreign key (idDireccion) references direccion(idDireccion)
);

create table loggs
(
id int auto_increment primary key,
tabla varchar (255),
usr varchar (255),
operation varchar (255),
id_afectado int,
datee date default (current_date())
);


