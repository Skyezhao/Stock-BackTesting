class TEST(object):
	def factor001():
        '''
        Excel line 3-6
        现金周转因子：衡量上市公司现金的回收速度
        1)销售现金比率 = 经营活动产生的现金流量净额/营业收入
        2)销售收现比 = 销售商品提供劳务收到的现金/营业收入
        3)应收账款周转率=（期初应收账款净额+期末应收账款净额）/（2*营业收入）
        4）存款周转率=（期初存货净额+期末存货净额）/（2*营业成本）
        '''
        #---------- 销售现金比率 -----------
        ncf =  C.item('net_cash_flows_oper_act')
        oper_rev =  I.item('oper_rev')
        receive_cash = C.item('cash_recp_sg_and_rs')

        ncf_d = misc.Daily_FS(ncf).reindex( idx )
        oper_rev_d = misc.Daily_FS(oper_rev).reindex( idx )
        receive_cash_d = misc.Daily_FS(receive_cash).reindex( idx )

        inv = fi(dtt0,dtt2).item('s_fa_invturn')
        ar = fi(dtt0,dtt2).item('s_fa_arturn')
        inv_d = misc.Daily_FS(inv).reindex( idx )
        ar_d = misc.Daily_FS(ar).reindex( idx )

        output = ncf_d / oper_rev_d + receive_cash_d / oper_rev_d + ar_d + inv_d 

        output = output.reindex(idx) * has_price 

        return output

    def factor002():

        '''
        Excel line 7-8
        现金偿还能力因子：衡量上市公司偿债能力
        1）经营现金流动负债比率 = 季度经营活动产生的现金流量净额/当季季末流动负债
        2）现金流动比率 = 季度总现金流量的净额/当季季末流动负债
        由于未找到季末流动负债数据，因此统一成去掉季末字眼
        '''

        #---------- 经营现金流动负债比率 -----------
        oper_cash = C.item('net_cash_flows_oper_act')
        liab = B.item('tot_cur_liab')

        oper_cash_d = misc.Daily_FS(oper_cash).reindex( idx )
        liab_d = misc.Daily_FS(liab).reindex( idx )

        outcome1 = oper_cash_d / liab_d

        #---------- 现金流动比率(计算投资及筹资）-----------
        inv_cash = C.item('net_cash_flows_inv_act')
        fnc_cash = C.item('net_cash_flows_fnc_act')

        inv_cash_d = misc.Daily_FS(inv_cash).reindex( idx )
        fnc_cash_d = misc.Daily_FS(fnc_cash).reindex( idx )

        outcome2 = (oper_cash_d + inv_cash_d + fnc_cash_d)/liab_d

        #---------- 因子计算 -----------
        outcome = (outcome1 + outcome2).reindex(idx) * has_price 

        return outcome

    def factor003():

        '''
        Excel line 9-11
        现金流质量因子：反映了上市公司现金流的结构是否合理
        1）经营质量=季度销售商品提供劳务收到的现金/季度经营现金流流入
        2）投资质量=（季度收回投资所收到的现金+季度取得投资收益所收到的现金）/季度投资现金流流入
        3）筹资质量=季度吸收投资所收到的现金/季度筹资现金流流入
        '''
        #---------- 经营质量 -----------
        receive_cash = C.item('cash_recp_sg_and_rs')
        oper_in = C.item('stot_cash_inflows_oper_act')

        receive_cash_d = misc.Daily_FS(receive_cash).reindex( idx )
        oper_in_d = misc.Daily_FS(oper_in).reindex( idx )

        factor1 = receive_cash_d / oper_in_d
        #---------- 投资质量 -----------
        withdraw = C.item('cash_recp_disp_withdrwl_invest')
        return_ = C.item('cash_recp_return_invest')
        inv_in = C.item('stot_cash_inflows_inv_act')

        withdraw_d = misc.Daily_FS(withdraw).reindex( idx )
        return__d = misc.Daily_FS(return_).reindex( idx )
        inv_in_d = misc.Daily_FS(inv_in).reindex( idx )

        factor2 = (withdraw_d + return__d) / inv_in_d
        #---------- 筹资质量 -----------
        contrib = C.item('cash_recp_cap_contrib')
        fnc_in = C.item('stot_cash_inflows_fnc_act')

        contrib_d = misc.Daily_FS(contrib).reindex( idx )
        fnc_in_d = misc.Daily_FS(fnc_in).reindex( idx )

        factor3 = contrib_d / fnc_in_d

        #---------- 因子计算 -----------
        outcome = (factor1 + factor2 + factor3).reindex(idx) * has_price 

        return outcome

    def factor004():

        '''
        Excel line 16
        现金流量市值比因子:研究现金流量市值比对股价后期走势的影响
        =经营活动产生的现金流量净额/总市值
        '''
        
        oper_cash = C.item('net_cash_flows_oper_act')
        oper_cash_d = misc.Daily_FS(oper_cash).reindex( idx )

        tcap = Quote(idx).get('tcap') * 10000
        outcome = oper_cash_d / tcap
        outcome = outcome.reindex(idx) * has_price

        return outcome

    def factor005():

        '''
        Excel line 19
        营业现金流价格比率
        = t月份末的营业现金流/t月份末的A股流通市值
        '''
        
        oper_cash = C.item('net_cash_flows_oper_act')
        oper_cash_d = misc.Daily_FS(oper_cash).reindex( idx )

        mcap = Quote(idx).get('mcap') * 10000  #取市值
        outcome = oper_cash_d / mcap
        outcome = outcome.reindex(idx) * has_price

        return outcome

    def factor006():

        '''
        Excel line 21
        增值变化（ACCP)
        =（利润总额-营业现金流）/净利润
        '''
        tot_profit = I.item('tot_profit')
        oper_cash = C.item('net_cash_flows_oper_act')
        net_profit = I.item('net_profit')

        tot_profit_d = misc.Daily_FS(tot_profit).reindex( idx )
        oper_cash_d = misc.Daily_FS(oper_cash).reindex( idx )
        net_profit_d = misc.Daily_FS(net_profit).reindex( idx )

        outcome = (tot_profit_d - oper_cash_d) / net_profit_d
        outcome = outcome.reindex(idx) * has_price

        return outcome

    def factor007():

        '''
        可操控性应计利润 = 营业利润-经营性净现金流
        '''

        oppro = I.item('oper_profit')
        ncf =  C.item('net_cash_flows_oper_act')

        oppro_d = misc.Daily_FS(oppro).reindex( idx )
        ncf_d = misc.Daily_FS(ncf).reindex( idx )

        outcome = (oppro_d - ncf_d).reindex(idx) * has_price

        return outcome

    def factor008(ddt1,ddt2):

        '''
        有形净值/带息负债
        '''

        net = List_df.nansum(B.item('tot_assets') - B.item('tot_liab') - B.item('intang_assets') - B.item('goodwill'))
        net_d = misc.Daily_FS(net).reindex( idx )

        debt = fi(dtt0,dtt2).item('s_fa_interestdebt')
        debt_d = misc.Daily_FS(debt).reindex( idx )

        output = oper_cash_d / debt_d
        output = output.reindex(idx) * has_price

        return output

    def factor009(ddt1,ddt2):
        '''
        有形资产/带息债务
        '''     
        debt_asset = fi(dtt0,dtt2).item('s_fa_tangassettointdebt')
        
        debt_asset_d = misc.Daily_FS(debt_asset).reindex( idx )
         
        output = debt_asset_d * has_price
        
        return output


    def factor010(dtt1,dtt2):
        '''
        带息债务/全部投入资产
        '''     
        debt_asset = fi(dtt0,dtt2).item('s_fa_intdebttototalcap')
        
        debt_asset_d = misc.Daily_FS(debt_asset).reindex( idx )
         
        output = debt_asset_d * has_price
        
        return output

    def factor011(dtt1,dtt2):
        '''
        归属母公司的股东权益/带息债务
        '''     
        debt_asset = fi(dtt0,dtt2).item('s_fa_equitytointerestdebt')
        
        debt_asset_d = misc.Daily_FS(debt_asset).reindex( idx )
         
        output = debt_asset_d * has_price
        
        return output

    def factor012(dtt1,dtt2):
        '''
        经营活动产生的现金流量净额/带息债务
        '''     
        debt_asset = fi(dtt0,dtt2).item('s_fa_ocftointerestdebt')
        
        debt_asset_d = misc.Daily_FS(debt_asset).reindex( idx )
         
        output = debt_asset_d * has_price
        
        return output

    def factor013(ddt1,ddt2):

        '''
        有形净值/净债务
        '''

        net = List_df.nansum(B.item('tot_assets') - B.item('tot_liab') - B.item('intang_assets') - B.item('goodwill'))
        net_d = misc.Daily_FS(net).reindex( idx )

        debt = fi(dtt0,dtt2).item('s_fa_netdebt')
        debt_d = misc.Daily_FS(debt).reindex( idx )

        output = oper_cash_d / debt_d
        output = output.reindex(idx) * has_price

        return output

    def factor014(dtt1,dtt2):
        '''
        有形资产/净债务
        '''     
        debt_asset = fi(dtt0,dtt2).item('s_fa_tangibleassettonetdebt')
        
        debt_asset_d = misc.Daily_FS(debt_asset).reindex( idx )
         
        output = debt_asset_d * has_price
        
        return output

    def factor015(ddt1,ddt2):

        '''
        研发成本
        =管理费用/流通市值
        '''
        admin = I.item('less_gerl_admin_exp')
        admin_d = misc.Daily_FS(admin).reindex( idx )

        mcap = Quote(idx).get('mcap') * 10000

        output = admin_d / mcap
        output = output.reindex(idx) * has_price

        return output


    def factor016(ddt1,ddt2):

        '''
        研发成本收入比
        =管理费用/营业收入
        '''

        admin = I.item('less_gerl_admin_exp')
        admin_d = misc.Daily_FS(admin).reindex( idx )

        oper = I.item('oper_rev')
        oper_d = misc.Daily_FS(oper).reindex( idx )

        output = admin_d / oper_d
        output = output.reindex(idx) * has_price

        return output

    def factor017(dd1,ddt2):

        '''
        流动市值/总市值
        '''

        mcap = Quote(idx).get('mcap') * 10000
        tcap = Quote(idx).get('tcap') * 10000

        output = mcap/tcap
        output = output.reindex(idx) * has_price

        return output

    def factor018(ddt1,ddt2):

        '''
        现金生产力
        =（流通市值+长期负债-总资产合计）/货币资金
        #无总资产合计，暂用流动资产合计替代
        '''
        mcap = Quote(idx).get('mcap') * 10000

        non_liab = B.item('tot_non_cur_liab')
        non_liab_d = misc.Daily_FS(non_liab).reindex( idx )

        cur_asset = B.item('tot_cur_assets')
        cur_asset_d = misc.Daily_FS(cur_asset).reindex( idx )

        money = B.item('monetary_cap')
        money_d = misc.Daily_FS(money).reindex( idx )

        output = (mcap + non_liab_d - cur_asset_d) / money_d
        output = output.reindex(idx) * has_price

        return output

    def factor019(ddt1,ddt2):

        '''
        现金资产比
        =t月货币资金/t-12月与t月的平均资产合计
        '''

        tot_assets = B.item('tot_assets') # 本期总资产
        tot_assets_last = tot_assets.shift(4) #12个月前的总资产
        avg=(tot_assets + tot_assets_last)/2 #平均资产总额
        avg_d = misc.Daily_FS(avg).reindex( idx )

        money = B.item('monetary_cap')
        money_d = misc.Daily_FS(money).reindex( idx )

        output = money_d/avg_d
        output = output.reindex(idx) * has_price

        return output

    def factor020(ddt1,ddt2):

        '''
        资本换手率
        =t月营业收入/t-12月资产合计
        '''
        tot_assets = B.item('tot_assets') # 本期总资产
        tot_assets_last = tot_assets.shift(4) #12个月前的总资产
        last_d = misc.Daily_FS(last).reindex( idx )

        oper = I.item('oper_rev')
        oper_d = misc.Daily_FS(oper).reindex( idx )

        output = oper_d/last_d
        output = output.reindex(idx) * has_price

        return output

    def factor021(ddt1,ddt2):

        '''
        股利价格比
        =应付股利/流通市值
        '''
        pay = B.item('dvd_payable')
        pay_d = misc.Daily_FS(pay).reindex( idx )
        mcap = Quote(idx).get('mcap') * 10000

        output = pay_d/mcap
        output = output.reindex(idx) * has_price

        return output

    def factor022(ddt1,ddt2):

        '''
        总负债市值比
        =总负债/流通市值
        '''
        liab = B.item('tot_liab')
        liab_d = misc.Daily_FS(liab).reindex( idx )
        mcap = Quote(idx).get('mcap') * 10000

        output = liab_d/mcap
        output = output.reindex(idx) * has_price

        return output

    def factor023(ddt1,ddt2):
        '''
        流动比率
        =去年12月底流动资产合计/去年12月底流动负债合计
        '''
        asset = B.item('tot_cur_assets')
        asset = asset[ asset.index.map(lambda x:x.month) == 12 ]
        asset_d = misc.Daily_FS(asset).reindex( idx )
        liab = B.item('tot_cur_liab')
        liab = liab[ liab.index.map(lambda x:x.month) == 12 ]
        liab_d = misc.Daily_FS(liab).reindex( idx )

        output = asset_d / liab_d
        output = output.reindex(idx) * has_price

        return output

    def factor024(ddt1,ddt2):

        '''
        流动比率增长率
        =t月-t-12月/t-12月
        '''
        asset = B.item('tot_cur_assets')
        asset = asset[ asset.index.map(lambda x:x.month) == 12 ]
        asset_d = misc.Daily_FS(asset).reindex( idx )
        liab = B.item('tot_cur_liab')
        liab = liab[ liab.index.map(lambda x:x.month) == 12 ]
        liab_d = misc.Daily_FS(liab).reindex( idx )

        liquid = asset_d / liab_d #求得流动比率
        liquid_last = liquid.shift(4).reindex( idx )

        output = (liquid - liquid_last)/liquid_last
        output = output.reindex(idx) * has_price

        return output