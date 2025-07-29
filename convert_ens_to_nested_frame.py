## Convert Single QP Ensemble to Nested Pandas Dataframe

def convert_ens_to_nested_frame(ens):
    """
    Converts a single qp.Ensemble object into a NestedFrame in nested-pandas format. 
    This function handles various distribution types (norm, mixmod, interp, hist, quant) by extracting and aligning metadata (e.g., xvals, bins, quants) with associated data arrays. 
    It flattens the structured data by object and index, then reconstructs it into a NestedFrame grouped by object_id, making it suitable for downstream nested-pandas operations.
    """
    import numpy as np
    import pandas as pd
    import nested_pandas as npd
    from nested_pandas.nestedframe import NestedFrame
    data_table = ens.build_tables()
    qp_type = data_table["meta"]["pdf_name"][0].astype(str)
    
    # Get the basic structure
    if qp_type == "norm" or qp_type == "mixmod":
        qp_dict = data_table["data"]
    elif qp_type == "interp":
        xvals = np.array(data_table["meta"]["xvals"])  # shape (301,)
        repeated_xvals = np.tile(xvals, (len(data_table["data"]["yvals"]), 1))
        xvals_dict = {"xvals": repeated_xvals}
        qp_dict = data_table["data"] | xvals_dict
    elif qp_type == "hist":
        bins = np.array(data_table["meta"]["bins"])
        repeated_bins = np.tile(bins, (len(data_table["data"]["pdfs"]), 1))
        bins_dict = {"bins": repeated_bins}
        qp_dict = data_table["data"] | bins_dict
    elif qp_type == "quant":
        quants = np.array(data_table["meta"]["quants"])  # shape (301,)
        repeated_quants = np.tile(quants, (len(data_table["data"]["locs"]), 1))
        quants_dict = {"quants": repeated_quants}
        qp_dict = data_table["data"] | quants_dict
    
    # Create flat data for nested-pandas
    flat_data = []
    
    first_key = next(iter(qp_dict))
    n_objects = len(qp_dict[first_key])
    
    for obj_idx in range(n_objects):
        for i in range(len(qp_dict[first_key][obj_idx])):  # iterate through array elements
            row_data = {'object_id': obj_idx}
            for key in qp_dict.keys():
                if key == "bins":
                    row_data[key] = qp_dict[key][obj_idx][i] if i < len(qp_dict[key][obj_idx]) - 1 else None
                else:
                    row_data[key] = qp_dict[key][obj_idx][i]
            if row_data.get(list(qp_dict.keys())[0]) is not None:  # Skip None values
                flat_data.append(row_data)
    
    # Convert to flat DataFrame
    flat_df = pd.DataFrame(flat_data)
    
    # Determine nested columns (all except object_id)
    nested_cols = [col for col in flat_df.columns if col != 'object_id']
    
    # Create NestedFrame
    nested_frame = NestedFrame.from_flat(
        flat_df,
        base_columns=[],  # No base columns except implicit index
        nested_columns=nested_cols,
        on='object_id',
        name=f'{qp_type}_data'
    )
    
    return nested_frame