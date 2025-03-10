-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: conjunto_residencial
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `casas`
--

DROP TABLE IF EXISTS `casas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `casas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `numero` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero` (`numero`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `casas`
--

LOCK TABLES `casas` WRITE;
/*!40000 ALTER TABLE `casas` DISABLE KEYS */;
INSERT INTO `casas` VALUES (1,'Torre 1 -101'),(2,'Torre 1 -102'),(3,'Torre 1 -103'),(4,'Torre 1 -104'),(5,'Torre 1 -201'),(6,'Torre 1 -202'),(7,'Torre 1 -203'),(8,'Torre 1 -204'),(9,'Torre 1 -301'),(10,'Torre 1 -302'),(11,'Torre 1 -303'),(12,'Torre 1 -304'),(13,'Torre 1 -401'),(14,'Torre 1 -402'),(15,'Torre 1 -403'),(16,'Torre 1 -404'),(17,'Torre 1 -501'),(18,'Torre 1 -502'),(19,'Torre 1 -503'),(20,'Torre 1 -504');
/*!40000 ALTER TABLE `casas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estado_reserva`
--

DROP TABLE IF EXISTS `estado_reserva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estado_reserva` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estado_reserva`
--

LOCK TABLES `estado_reserva` WRITE;
/*!40000 ALTER TABLE `estado_reserva` DISABLE KEYS */;
INSERT INTO `estado_reserva` VALUES (2,'Confirmada'),(3,'Espera de Aprobación'),(1,'Pendiente');
/*!40000 ALTER TABLE `estado_reserva` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estados_factura`
--

DROP TABLE IF EXISTS `estados_factura`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estados_factura` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estados_factura`
--

LOCK TABLES `estados_factura` WRITE;
/*!40000 ALTER TABLE `estados_factura` DISABLE KEYS */;
INSERT INTO `estados_factura` VALUES (2,'Pagada'),(1,'Pendiente'),(3,'Vencida');
/*!40000 ALTER TABLE `estados_factura` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estados_pqrs`
--

DROP TABLE IF EXISTS `estados_pqrs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estados_pqrs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estados_pqrs`
--

LOCK TABLES `estados_pqrs` WRITE;
/*!40000 ALTER TABLE `estados_pqrs` DISABLE KEYS */;
INSERT INTO `estados_pqrs` VALUES (2,'En Proceso'),(1,'Registrada'),(3,'Resuelta');
/*!40000 ALTER TABLE `estados_pqrs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facturas`
--

DROP TABLE IF EXISTS `facturas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facturas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_solicitud` int NOT NULL,
  `id_usuario` int NOT NULL,
  `fecha_emision` date NOT NULL,
  `monto` float NOT NULL,
  `comprobante_pago` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `facturas_ibfk_2_idx` (`id_usuario`),
  KEY `facturas_ibfk_1_idx` (`id_solicitud`),
  CONSTRAINT `facturas_ibfk_1` FOREIGN KEY (`id_solicitud`) REFERENCES `reserva` (`id`),
  CONSTRAINT `facturas_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facturas`
--

LOCK TABLES `facturas` WRITE;
/*!40000 ALTER TABLE `facturas` DISABLE KEYS */;
INSERT INTO `facturas` VALUES (1,1,2,'2025-02-28',50000,NULL),(2,1,2,'2025-02-28',50000,NULL),(3,1,2,'2025-02-28',50000,NULL),(4,1,2,'2025-02-28',50000,NULL),(5,1,2,'2025-02-28',50000,NULL),(6,1,2,'2025-02-28',50000,NULL),(8,1,2,'2025-02-28',50000,NULL),(9,1,2,'2025-02-28',50000,NULL),(10,1,2,'2025-02-28',50000,NULL),(11,1,2,'2025-02-28',50000,NULL),(25,8,2,'2025-03-03',50000,NULL),(26,9,2,'2025-03-06',50000,NULL);
/*!40000 ALTER TABLE `facturas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pagos`
--

DROP TABLE IF EXISTS `pagos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_factura` int NOT NULL,
  `fecha_pago` date NOT NULL,
  `monto_pagado` decimal(10,2) NOT NULL,
  `metodo_pago` enum('Efectivo','Transferencia','Tarjeta') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_factura` (`id_factura`),
  CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`id_factura`) REFERENCES `facturas` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagos`
--

LOCK TABLES `pagos` WRITE;
/*!40000 ALTER TABLE `pagos` DISABLE KEYS */;
/*!40000 ALTER TABLE `pagos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pqrs`
--

DROP TABLE IF EXISTS `pqrs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pqrs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `tipo` enum('Petición','Queja','Reclamo','Sugerencia') NOT NULL,
  `descripcion` text NOT NULL,
  `id_estado` int NOT NULL,
  `respuesta` text,
  `fecha_respuesta` timestamp NULL DEFAULT NULL,
  `id_tipo` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_estado` (`id_estado`) /*!80000 INVISIBLE */,
  KEY `id_tipo` (`id_tipo`),
  CONSTRAINT `pqrs_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pqrs_ibfk_2` FOREIGN KEY (`id_estado`) REFERENCES `estados_pqrs` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `pqrs_ibfk_3` FOREIGN KEY (`id_tipo`) REFERENCES `tipo_pqrs` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pqrs`
--

LOCK TABLES `pqrs` WRITE;
/*!40000 ALTER TABLE `pqrs` DISABLE KEYS */;
/*!40000 ALTER TABLE `pqrs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reserva`
--

DROP TABLE IF EXISTS `reserva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `fecha` date NOT NULL,
  `horario` varchar(30) NOT NULL,
  `descripcion` varchar(300) NOT NULL,
  `id_estado` int NOT NULL,
  `comprobante_pago` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_estado` (`id_estado`),
  CONSTRAINT `reserva_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `reserva_ibfk_2` FOREIGN KEY (`id_estado`) REFERENCES `estado_reserva` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva`
--

LOCK TABLES `reserva` WRITE;
/*!40000 ALTER TABLE `reserva` DISABLE KEYS */;
INSERT INTO `reserva` VALUES (1,2,'2025-02-28','18:00:00','18:59:00',2,'Colsubsidio_Debito_PSE_Febrero.pdf'),(8,2,'2025-03-04','10:00:00','12:00:00',2,'EndPoints.pdf'),(9,2,'2025-03-12','12:43:00','13:43:00',2,'EndPoints1.pdf');
/*!40000 ALTER TABLE `reserva` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (2,'Administrador'),(1,'Residente');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_pqrs`
--

DROP TABLE IF EXISTS `tipo_pqrs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_pqrs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_pqrs`
--

LOCK TABLES `tipo_pqrs` WRITE;
/*!40000 ALTER TABLE `tipo_pqrs` DISABLE KEYS */;
INSERT INTO `tipo_pqrs` VALUES (1,'Peticion'),(2,'Queja'),(3,'Reclamos'),(4,'Sugerencias');
/*!40000 ALTER TABLE `tipo_pqrs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `id_rol` int NOT NULL,
  `id_casa` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `id_rol` (`id_rol`),
  KEY `id_casa` (`id_casa`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `usuarios_ibfk_2` FOREIGN KEY (`id_casa`) REFERENCES `casas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'admin','prueba@gmail.com','scrypt:32768:8:1$oFnvAodkb387431C$c2826ae32d91387322ce562374dba140b8fc15f5a83ad63af2520aa388ef201f3f0295705e08a3524c819d7e34dddb62e0e4828a2a28f89a415d191c2164b826','3245123566',2,1),(2,'prueba','prueba1@gmail.com','scrypt:32768:8:1$AJt13ukYWsCAsheM$76c90bda5fb9a519992cb811aac38a29709fe592752c57610ac398100d331cbd6adf20900f6a37321289e263022dcc65ee9e6f935fbd463d66a68b527721eedf','123',1,2);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-09 23:15:18
