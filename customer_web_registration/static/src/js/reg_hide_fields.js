odoo.define('customer_web_registration.reg_hide_fields', function (require) {
'use strict';

		$(document).ready(function () {
			$("#companyC").attr('checked', 'checked');
			$("#personP").attr('checked', 'checked');

			//  company fields hide when select individual in sign up form
			var CompanyTypeFields = '#mph62d0lw8, #wac861iw3un, #weibh1m8ztk, #kxbiabcfnso, #kxbipzmfnso, #50u6nr8im5f, #c63pr9w5c5g, #50u6nr8im5Sp, #ae7rhibv80p, #50u6nr8im5dls, #kn6ol6bkha, #bt2ecs7fdb5, #leesgs3fz4p, #nzslz27anz, #zw16omomxh, #vdhbc63avj, #jasbu73bow, #slvbo83jdo';

			//  company fields hide when select company in sign up form
			var PersonTypeFields = '#m9ciyengx5h, #de5f9s72dfq, #r930uuel4ss, #pzgeuspbd6, #fpqo7z5bomu, #y20fu2e011, #tpdlzie70l, #bvhsnk52ndj, #vcjas623jhv, #bscs72ko, #nskeu63kd7l, #k8sem1t93a8, #v2732cp5atl, #pdmxc4actq, #wppoowblfyg';		

			$("#company").on('click',function(e)
			{
				var CompanyType = $("#company").val();
				var PersonType = $("#person").val();
				// select company, hide individual fields in sign up form
				if (CompanyType == 'company')
					{
						window.open('/web/signup','_self');
			        }
			});
			
			$("#person").on('click',function(e)
			{
				var CompanyType = $("#company").val();
				var PersonType = $("#person").val();
				// select individual, hide company fields in sign up form
				if (PersonType == 'person')
					{
					window.open('/web/signup/individual','_self');
			        }
			});			
		});
});
