from Scripts import pysmart_basic as psb


plotter = psb.PySmartBasicPlotter()
plotter.save_attributes_to_json("smart_attributes.json")

psb.PySmartBasicPlotter.load_and_plot_from_json("smart_attributes.json")
