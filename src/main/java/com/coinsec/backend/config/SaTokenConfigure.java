package com.coinsec.backend.config;

import cn.dev33.satoken.interceptor.SaInterceptor;
import cn.dev33.satoken.router.SaRouter;
import cn.dev33.satoken.stp.StpUtil;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * <p>
 * SaTokenConfigure 配置类
 * </p>
 *
 * @author kody
 * @since 2025-10-16
 */
@Configuration
public class SaTokenConfigure implements WebMvcConfigurer {

	/**
	 * 注册 Sa-Token 拦截器，打开注解式鉴权功能
	 */
	@Override
	public void addInterceptors(InterceptorRegistry registry) {
		registry.addInterceptor(new SaInterceptor(handler -> SaRouter
				.match("/**")
				.notMatch("/auth/users/login", "/auth/users/register")
				.check(r -> StpUtil.checkLogin()))).addPathPatterns("/**");
	}
}