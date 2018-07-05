class ReadsParser {

  constructor(data_from_fetch) {
    //datasets/
    this.data_from_fetch = data_from_fetch;

    //datasets/{df}/
    this.df = this.data_from_fetch.children[0]['node_name'];

    //datasets/{df}/reads/{preproc}
    this.preproc = this.data_from_fetch.children[0].children[0].children[0]['node_name'];

    console.log(this.df);
    console.log(this.preproc);

    this.samples_for_preproc = this.parseReadsFolder(this.data_from_fetch.children[0].children[0].children[0]);
    console.log(this.samples_for_preproc);

  }

  get preprocs() {
    let preprocs = [];
    for (let i = 0; i < this.data_from_fetch.children[0].children[0]['children'].length; i++) {
      preprocs.push(this.data_from_fetch.children[0].children[0].children[i]['node_name'])
    }
    return preprocs;
  }

  reads_for_preproc(preproc) {
    let reads_ar = [];
    let df_reads_all = this.data_from_fetch.children[0].children[0].children;

    for (let i = 0; i < df_reads_all.length; i++) {
      const preproc_i_node = df_reads_all[i];
      if (preproc_i_node['node_name'] === preproc) {
        if (preproc_i_node['children'].length > 0) {
          for (let i = 0; i < preproc_i_node['children'].length; i++) {
            reads_ar.push(this.parseSampleFolder(preproc_i_node['children'][i]))
          }
        }
      }
    }

    return reads_ar
  }

  parseSampleFolder(fsNode) {
    let sample = {};
    sample.sample_name = fsNode['node_name'];
    sample.files = [];
    let r1_size = '';
    let r2_size = '';
    let bp = 0;
    let reads = 0;
    for (let i = 0; i < fsNode['children'].length; i++) {
      let file = this.parseFSNode(fsNode['children'][i]);
      if (file['node_name'].includes('_R1')) {
        r1_size = file['size']
      }
      else if (file['node_name'].includes('_R2')) {
        r2_size = file['size']
      }
      bp += parseInt(file['bp']);
      reads += parseInt(file['reads']);
    }
    sample.r1_size = r1_size;
    sample.r2_size = r2_size;
    sample.bp = bp;
    sample.reads = reads;
    return (sample);
  };

  parseReadsFolder(fsNode) {
    let reads_ar = [];
    if (fsNode.hasOwnProperty('children')) {
      if (fsNode['children'].length > 0) {
        for (let i = 0; i < fsNode['children'].length; i++) {
          reads_ar.push(this.parseSampleFolder(fsNode['children'][i]))
        }
      }
    }
    return reads_ar
  };


  parseFSNode = (fsNode) => {
    if (fsNode['type'] === 'dir') {
      if (fsNode.hasOwnProperty('children')) {
        if (fsNode['children'].length > 0) {
          if (fsNode['level'] === 3) {
            let sample_data = this.parseReadsFolder(fsNode);
            let data = this.state.data;
            data.push(sample_data);
            this.setState({['data']: data});
            return sample_data;
          }
          else {
            for (let i = 0; i < fsNode['children'].length; i++) {
              this.parseFSNode(fsNode['children'][i])
            }
          }
        }
        return fsNode;
      }
    }
    else if (fsNode['type'] === 'file') {
      return fsNode;
    }
  };
}

export default ReadsParser