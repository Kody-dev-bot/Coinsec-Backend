package com.coinsec.backend;

import com.baomidou.mybatisplus.generator.FastAutoGenerator;
import com.baomidou.mybatisplus.generator.config.OutputFile;
import com.baomidou.mybatisplus.generator.engine.FreemarkerTemplateEngine;

import java.util.Collections;

/**
 * <p>
 * CodeGenerator is the main class of the code generator.
 * </p>
 *
 * @author kody
 * @since 2025-10-16
 */
public class CodeGenerator {

	private static final String DB_USERNAME = System.getenv("DB_USERNAME");
	private static final String DB_PASSWORD = System.getenv("DB_PASSWORD");
	private static final String DB_URL = System.getenv("DB_URL");

	/**
	 * 项目路径
	 */
	private static final String PROJECT_PATH = System.getProperty("user.dir") + "/src/main";
	/**
	 * 输出目录
	 */
	private static final String OUTPUT_DIR = PROJECT_PATH + "/java";
	/**
	 * xml输出目录
	 */
	private static final String XML_OUTPUT_PATH = PROJECT_PATH + "/resources/xml";

	public static void main(String[] args) {
		FastAutoGenerator.create(DB_URL, DB_USERNAME, DB_PASSWORD)
				.globalConfig(builder -> builder
						.author("kody")
						.outputDir(OUTPUT_DIR)
						.commentDate("yyyy-MM-dd")
				)
				.packageConfig(builder -> builder
						.moduleName("auth")
						.parent("com.coinsec.backend")
						.entity("entity")
						.mapper("mapper")
						.xml("")
						.pathInfo(Collections.singletonMap(OutputFile.xml, XML_OUTPUT_PATH))
						.service("service")
						.serviceImpl("service.impl")
				)
				.strategyConfig(builder -> builder
						.enableCapitalMode()
						.enableSkipView()
						.disableSqlFilter()
						.addInclude("users")

						// entity
						.entityBuilder()
						.enableLombok()
						.enableRemoveIsPrefix()
						.enableTableFieldAnnotation()
						.enableActiveRecord()
						.versionColumnName("version")
						.formatFileName("%sEntity")

						// controller
						.controllerBuilder()
						.enableHyphenStyle()
						.enableRestStyle()
						.formatFileName("%sController")

						// service
						.serviceBuilder()
						.formatServiceFileName("%sService")
						.formatServiceImplFileName("%sServiceImpl")

						// mapper
						.mapperBuilder()
						.formatMapperFileName("%sMapper")
						.formatXmlFileName("%sXml")
				)
				.templateEngine(new FreemarkerTemplateEngine())
				.execute();
	}
}