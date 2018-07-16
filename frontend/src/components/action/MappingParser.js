class MappingParser {
  constructor(mapping_fs) {
    this.mapping_fs = mapping_fs;
  }

  get datasets() {
    let dfs = [];
    for (let i = 0; i < this.mapping_fs['children'].length; i++) {
      dfs.push(this.mapping_fs.children[i]['node_name'])
    }
    return dfs;
  }

  preprocs_for_df(df) {
    let preprocs = [];
    for (let i = 0; i < this.mapping_fs['children'].length; i++) {
      if (this.mapping_fs.children[i]['node_name'] === df) {
        let preprocs_node = this.mapping_fs.children[i].children[0];
        for (let i = 0; i < preprocs_node['children'].length; i++) {
          preprocs.push(preprocs_node.children[i]['node_name'])
        }
      }
    }
    return preprocs;
  }

  tools_for_preproc(df, preproc) {
    let tools = [];
    for (let i = 0; i < this.mapping_fs['children'].length; i++) {
      if (this.mapping_fs.children[i]['node_name'] === df) {
        let preprocs_node = this.mapping_fs.children[i].children[0];
        for (let i = 0; i < preprocs_node['children'].length; i++) {
          if (preprocs_node.children[i]['node_name'] === preproc) {
            let tools_node = preprocs_node.children[i];
            for (let i = 0; i < tools_node['children'].length; i++) {
              tools.push(tools_node.children[i]['node_name'])
            }
          }
        }
      }
    }
    return tools;
  }

  postprocs_for_tool(df, preproc, tool) {
    let postprocs = [];
    for (let i = 0; i < this.mapping_fs['children'].length; i++) {
      if (this.mapping_fs.children[i]['node_name'] === df) {
        let preprocs_node = this.mapping_fs.children[i].children[0];
        for (let i = 0; i < preprocs_node['children'].length; i++) {
          if (preprocs_node.children[i]['node_name'] === preproc) {
            let tools_node = preprocs_node.children[i];
            for (let i = 0; i < tools_node['children'].length; i++) {
              if (tools_node.children[i]['node_name'] === tool) {
                let postproc_node = tools_node.children[i].children[0].children[0];
                for (let i = 0; i < postproc_node['children'].length; i++) {
                  postprocs.push(postproc_node.children[i]['node_name'])
                }
              }
            }
          }
        }
      }
    }
    return postprocs;
  }

  samples_for_post(df, preproc, tool, post) {
    let samples = [];
    for (let i = 0; i < this.mapping_fs['children'].length; i++) {
      if (this.mapping_fs.children[i]['node_name'] === df) {
        let preprocs_node = this.mapping_fs.children[i].children[0];
        for (let i = 0; i < preprocs_node['children'].length; i++) {
          if (preprocs_node.children[i]['node_name'] === preproc) {
            let tools_node = preprocs_node.children[i];
            for (let i = 0; i < tools_node['children'].length; i++) {
              if (tools_node.children[i]['node_name'] === tool) {
                let postproc_node = tools_node.children[i].children[0].children[0];
                for (let i = 0; i < postproc_node['children'].length; i++) {
                  if (postproc_node.children[i]['node_name'] === post) {
                    let samples_node = postproc_node.children[i];
                    for (let i = 0; i < samples_node['children'].length; i++) {
                      samples.push(samples_node.children[i]['node_name'].split('.')[0])
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    return samples;
  }
}

export default MappingParser;