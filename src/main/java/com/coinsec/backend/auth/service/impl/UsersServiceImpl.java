package com.coinsec.backend.auth.service.impl;

import com.coinsec.backend.auth.entity.UsersEntity;
import com.coinsec.backend.auth.mapper.UsersMapper;
import com.coinsec.backend.auth.service.UsersService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

/**
 * <p>
 * 用户主表 服务实现类
 * </p>
 *
 * @author kody
 * @since 2025-10-16
 */
@Service
public class UsersServiceImpl extends ServiceImpl<UsersMapper, UsersEntity> implements UsersService {

}
