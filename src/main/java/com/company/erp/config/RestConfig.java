package com.company.erp.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.http.MediaType;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.http.converter.ByteArrayHttpMessageConverter;
import org.springframework.http.converter.FormHttpMessageConverter;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.http.converter.StringHttpMessageConverter;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.retry.annotation.EnableRetry;
import org.springframework.web.client.RestClient;

import java.nio.charset.StandardCharsets;
import java.util.List;

@Configuration
@EnableRetry
public class RestConfig {

    @Bean
    @Primary
    public RestClient restClient() {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(5000); // 5 секунд на установку соединения
        factory.setReadTimeout(10000);   // 10 секунд на чтение ответа

        return RestClient.builder()
                .requestFactory(factory)
                .messageConverters(converters -> converters.addAll(getMessageConverters()))
                .build();
    }

    private List<HttpMessageConverter<?>> getMessageConverters() {
        return List.of(
                createJacksonMapper(),
                new StringHttpMessageConverter(StandardCharsets.UTF_8),
                new FormHttpMessageConverter(),
                new ByteArrayHttpMessageConverter()
        );
    }

    private MappingJackson2HttpMessageConverter createJacksonMapper() {
        MappingJackson2HttpMessageConverter jackson2HttpMessageConverter = new MappingJackson2HttpMessageConverter();
        jackson2HttpMessageConverter.setSupportedMediaTypes(List.of(MediaType.ALL));
        return jackson2HttpMessageConverter;
    }
}

