import React, { Component } from "react";
import ListTable from "../components/listTable";
import { Button } from "@material-ui/core";
import Image from "../components/Image";

class VideoPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selected: null
    };
  }

  upload = e => {
    console.log(e);
  };

  render() {
    return (
      <section>
        <Image />
        <section
          style={{
            paddingTop: "30vh",
            paddingLeft: "20vw"
          }}
        >
          <Button
            variant="outlined"
            component="span"
            style={{
              marginBottom: "1%",
              color: "white",
              borderColor: "white",
              border: "solid"
            }}
          >
            Upload
          </Button>
        </section>

        <section
          style={{
            paddingLeft: "20vw"
          }}
        >
          <ListTable selected={this.state.selected} />
        </section>
      </section>
    );
  }
}

export default VideoPage;
