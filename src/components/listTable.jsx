import React, { Component } from "react"
import {
  Paper,
  Card,
  CardContent,
  Typography,
  CardActions,
  Button,
  withStyles,
} from "@material-ui/core"
import Axios from "axios"

const styles = {
  paper: {
    width: "50%",
    height: "50vh",
    overflowY: "auto",
    backgroundColor: "transparent",
  },
}

class ListTable extends Component {
  constructor(props) {
    super(props)
    this.state = {
      job_list: [],
    }
  }

  componentWillMount() {
    this.updateList()
    this.timer = setInterval(() => this.updateList(), 5000)
  }

  componentWillUnmount() {
    clearInterval(this.timer)
  }

  updateList = () => {
    Axios.get("http://127.0.0.1:5000/list")
      .then(res => {
        this.setState({ job_list: res["data"] })
      })
      .catch(err => {
        console.log(err)
      })
  }

  render() {
    return (
      <Paper className={this.props.classes.paper}>
        {this.state.job_list.map(row => (
          <Card key={row[0]} className="card">
            <CardContent>
              <Typography variant="h5" component="h2">
                Video ID: {row[0]}
              </Typography>
              <Typography variant="h6" component="h2">
                Status: {row[1] === 0 ? "In Progress" : "Finished"}
              </Typography>
            </CardContent>
            <CardActions>
              <Button variant="contained" color="primary">
                View Details
              </Button>
            </CardActions>
          </Card>
        ))}
      </Paper>
    )
  }
}

export default withStyles(styles)(ListTable)
