def DEscreener_getdata(DE_level: str, primary_site: str, project: str, DE_filter:list) -> list:
    condition1 = DE_filter[0].split('|')[0]
    condition2 = DE_filter[1].split('|')[0]
    condition1_count = DE_filter[0].split('|')[2]
    condition2_count = DE_filter[1].split('|')[2]
    FC_select = DE_filter[2].strip()
    FC_input = DE_filter[3].strip()
    TEST_select = DE_filter[4]
    TESTstates_select = DE_filter[5].split(' (')[0].strip()
    cor_method = DE_filter[6].strip()
    TEST_input = DE_filter[7].strip()
    FC_input = float(FC_input) if FC_input else FC_input
    TEST_input = float(TEST_input) if TEST_input else TEST_input
    stage_to_num_dict = {
        'normal' :'n',
		'stage i' : '1',
		'stage ii' : '2',
		'stage iii' : '3',
		'stage iv' : '4',
	}
    table_name_cuffdiff = "%s_%s_%s_%s"%(project,stage_to_num_dict[condition1],stage_to_num_dict[condition2],DE_level)
    print(table_name_cuffdiff)
    print(f"TESTstates_select: {TESTstates_select}")
    if TESTstates_select == "Greater":
        # "Greater (Condition2 > Condition1)"
        TEST_column = "%s_%s"%(TEST_select.replace(' ','_'),"greater")
    else: # "Less (Condition2 < Condition1)"
        TEST_column = "%s_%s"%(TEST_select.replace(' ','_'),'less')    
    if cor_method == "FDR": 
        TEST_column += "(fdr_bh)"
    elif cor_method == "Bonferroni":
        TEST_column += "(bonferroni)"
    print(TEST_column)
    DE_df = pd.read_csv(f"{current_path}/../static/data/DE_data/{stage_to_num_dict[condition1]}_{stage_to_num_dict[condition2]}corr_test_result_web_ver.csv")
    # print(DE_df[DE_df["foldchange"] == np.inf])
    ## filter by q-value
    if TEST_input != '':
        DE_df = DE_df[DE_df[TEST_column] <= TEST_input]
    else: 
        pass
    ## filter by foldchange
    DE_df = DE_df[DE_df["foldchange"] >= 0.001]
    if FC_select == '≥':
        DE_df = DE_df[(DE_df["foldchange"] >= FC_input) & (DE_df["foldchange"] != np.inf)]
    elif FC_select == '≤':
        DE_df = DE_df[(DE_df["foldchange"] <= FC_input) & (DE_df["foldchange"] != np.inf)]
    else:
        pass
    DE_df = DE_df[['gene_name',TEST_column, 'avg_f_FPKM', 'avg_s_FPKM', 'foldchange']]
    DE_df['foldchange'] = DE_df['foldchange'].round(5)
    DE_df.replace(np.inf, '-', inplace=True)
    
    # print(DE_df["foldchange"].values.tolist())
    # diff_data,download_table_data, table_column = Filter.filter_logFC_Pvalue(TEST_column,table_name_cuffdiff,FC_select,FC_input,TEST_input,DE_level)
    if len(DE_df) != 0:
        return DE_df.values.tolist(), list(DE_df.columns), TEST_column
    else:
        return [], list(DE_df.columns), TEST_column