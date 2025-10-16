package com.coinsec.backend.auth.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.baomidou.mybatisplus.extension.activerecord.Model;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.io.Serial;
import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * <p>
 * 用户主表
 * </p>
 *
 * @author kody
 * @since 2025-10-16
 */
@Getter
@Setter
@ToString
@TableName("users")
public class UsersEntity extends Model<UsersEntity> {

	@Serial
	private static final long serialVersionUID = 1L;

	@TableId(value = "id", type = IdType.AUTO)
	private Integer id;

	/**
	 * 登录用户名，区分大小写
	 */
	@TableField("user_name")
	private String userName;

	/**
	 * bcrypt 加密后的密码
	 */
	@TableField("pwd_hash")
	private String pwdHash;

	@TableField("created_at")
	private LocalDateTime createdAt;

	@Override
	public Serializable pkVal() {
		return this.id;
	}
}
