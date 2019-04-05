import "./layout.css"
import Grid from "@material-ui/core/Grid"
import Button from "@material-ui/core/Button"

import React, { Component } from "react"
import Webcam from "react-webcam"
import io from "socket.io-client"
import AUTable from "../components/auTable"
const uuidv4 = require("uuid/v4")

class CameraPage extends Component {
  constructor(props) {
    super(props)
    this.promise = Promise.resolve(true)
    this.state = {
      promise: Promise.resolve(true),
      socket: io.connect("https://8966c50b.ngrok.io"),
      width: 0,
      height: 0,
      classification: {},
      regression: {},
      file_id: "",
    }
    this.state.socket.on("connect", () => {
      console.log("connected")
    })
    this.state.socket.on("message", message => {
      console.log(message)
      let data = JSON.parse(message[1])
      let regressionData = {}
      let classificationData = {}
      Object.keys(data).forEach(key => {
        if (key.includes("Regression")) {
          regressionData[key] = data[key]
        } else {
          classificationData[key] = data[key]
        }
      })
      this.setState({
        file_id: message[0],
        regression: regressionData,
        classification: classificationData,
      })
    })
  }

  componentDidMount() {
    this.updateDimensions()
    window.addEventListener("resize", this.updateDimensions)
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.updateDimensions)
  }

  updateDimensions = () => {
    this.setState({ width: window.innerWidth / 2, height: window.innerHeight })
  }

  setReference = webcam => {
    this.webcam = webcam
  }

  startTimer = () => {
    this.getAnalysis()
    this.timer = setInterval(() => this.getAnalysis(), 3000)
  }

  clearTimer = () => {
    clearInterval(this.timer)
  }

  getAnalysis = () => {
    if (this.webcam) {
      this.promise = this.promise.then(() => {
        return new Promise(resolve => {
          let image = this.webcam.getScreenshot()
          console.log(image)
          this.state.socket.send(image, uuidv4())
          resolve()
        })
      })
    }
  }

  render() {
    return (
      <Grid container spacing={40}>
        <Grid item xs={6}>
          <Webcam
            audio={false}
            ref={this.setReference}
            screenshotFormat="image/jpeg"
          />
        </Grid>
        <Grid item xs={6}>
          <Grid container alignItems="flex-start" justify="space-evenly">
            <Grid item xs={3} className={"primary"}>
              <Button
                variant="contained"
                color="primary"
                onClick={this.startTimer}
              >
                Start Analysis
              </Button>
            </Grid>
            <Grid item xs={3} className={"secondary"}>
              <Button
                variant="contained"
                color="secondary"
                onClick={this.clearTimer}
              >
                Stop Analysis
              </Button>
            </Grid>
          </Grid>
          <Grid
            container
            alignItems="flex-start"
            justify="space-evenly"
            className="container"
          >
            <Grid item xs={3}>
              <AUTable id={this.state.file_id} data={this.state.regression} />
            </Grid>
            <Grid item xs={3}>
              <AUTable
                id={this.state.file_id}
                data={this.state.classification}
              />
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    )
  }
}

export default CameraPage
