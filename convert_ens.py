## Convert QP Ensemble Storage Types

def convert_ens(ens, algo):
    """
    Converts a qp.Ensemble object into a dictionary of nested-pandas NestedFrame objects, using a consistent naming convention based on the algorithm and distribution type. 
    It preserves the original ensemble and additionally performs conversions between supported distribution types (interp, norm, mixmod) into histograms, quantiles (with varying resolutions), interpolations, and normal approximations. 
    Each result is stored in a structured format compatible with nested-pandas for easier downstream analysis and visualization.
    """
    import numpy as np
    import qp
    import convert_ens_to_nested_frame
    data_table = ens.build_tables()
    qp_type = data_table['meta']['pdf_name'][0].astype(str)
    converted_ensembles = {}
    
    # Store the original ensemble as nested-pandas NestedFrame
    converted_ensembles[f'{algo}_ens_{qp_type}'] = convert_ens_to_nested_frame.convert_ens_to_nested_frame(ens)
    
    # Define conversion parameters (same as original)
    bins = np.linspace(0, 3, 301)
    quantile_lengths = [99, 20, 5]
    
    if qp_type == 'interp':
        # Convert to histogram
        hist_ens = ens.convert_to(qp.hist_gen, bins=bins)
        converted_ensembles[f'{algo}_ens_{qp_type}_to_hist'] = convert_ens_to_nested_frame.convert_ens_to_nested_frame(hist_ens)
        
        # Convert to quantiles
        for qlen in quantile_lengths:
            quants = np.linspace(0.01, 0.99, qlen)
            var_name = f"{algo}_ens_{qp_type}_to_quant_{qlen}"
            try:
                print('here')
                quant_ens = ens.convert_to(qp.quant_gen, quants=quants)
                converted_ensembles[var_name] = convert_ens_to_nested_frame.convert_ens_to_nested_frame(quant_ens)
                print(f"Successfully created {var_name}")
            except Exception as e:
                print(f"Failed to create {var_name}: {e}")
        
        # Convert to normal distribution
        zmean = ens.mean()
        std = ens.std()
        norm_ens = qp.Ensemble(qp.stats.norm, data=dict(loc=zmean, scale=std))
        converted_ensembles[f'{algo}_ens_{qp_type}_to_norm'] = convert_ens_to_nested_frame.convert_ens_to_nested_frame(norm_ens)
        
    elif qp_type == 'norm':
        # Convert to histogram
        hist_ens = ens.convert_to(qp.hist_gen, bins=bins)
        converted_ensembles[f'{algo}_ens_{qp_type}_to_hist'] = convert_ens_to_nested_frame.convert_ens_to_nested_frame(hist_ens)
        
        # Convert to quantiles
        for qlen in quantile_lengths:
            quants = np.linspace(0.01, 0.99, qlen)
            var_name = f"{algo}_ens_{qp_type}_to_quant_{qlen}"
            try:
                print('here')
                quant_ens = ens.convert_to(qp.quant_gen, quants=quants)
                converted_ensembles[var_name] = convert_ens_to_nested_frame.convert_ens_to_nested_frame(quant_ens)
                print(f"Successfully created {var_name}")
            except Exception as e:
                print(f"Failed to create {var_name}: {e}")
        
        # Convert to interpolation
        interp_ens = ens.convert_to(qp.interp_gen, xvals=bins)
        converted_ensembles[f'{algo}_ens_{qp_type}_to_interp'] = convert_ens_to_nested_frame.convert_ens_to_nested_frame(interp_ens)
        
    elif qp_type == 'mixmod':
        # Convert to histogram
        hist_ens = ens.convert_to(qp.hist_gen, bins=bins)
        converted_ensembles[f'{algo}_ens_{qp_type}_to_hist'] = convert_ens_to_nested_frame.convert_ens_to_nested_frame(hist_ens)
        
        # Convert to quantiles
        for qlen in quantile_lengths:
            quants = np.linspace(0.01, 0.99, qlen)
            var_name = f"{algo}_ens_{qp_type}_to_quant_{qlen}"
            try:
                print('here')
                quant_ens = ens.convert_to(qp.quant_gen, quants=quants)
                converted_ensembles[var_name] = convert_ens_to_nested_frame.convert_ens_to_nested_frame(quant_ens)
                print(f"Successfully created {var_name}")
            except Exception as e:
                print(f"Failed to create {var_name}: {e}")
        
        # Convert to interpolation
        interp_ens = ens.convert_to(qp.interp_gen, xvals=bins)
        converted_ensembles[f'{algo}_ens_{qp_type}_to_interp'] = convert_ens_to_nested_frame.convert_ens_to_nested_frame(interp_ens)
    
    print("Done converting.")
    return converted_ensembles