USE `worldbankdb$eaphnl`;

LOCK TABLES `questionnaire_form` WRITE;
/*!40000 ALTER TABLE `questionnaire_form` DISABLE KEYS */;
INSERT INTO `questionnaire_form` VALUES (6,'Sputum Shipment Form ','sputum-shipment-form','Sputum Shipment collection Form','1','2013-03-05','',2),(7,'STUDY CLINICAL FORM (INTER/INTRA CLINICAL FORM)','study-clinical-form-interintra-clinical-form','INTER/INTRA CLINICAL FORM','2014','2014-10-12','',2),(8,'CLINICAL INFORMATION FORM','clinical-information-form','INFORMATION FORM','2014','2014-10-12','',2);
/*!40000 ALTER TABLE `questionnaire_form` ENABLE KEYS */;
UNLOCK TABLES;

-- Dump completed on 2014-12-15 13:52:37
