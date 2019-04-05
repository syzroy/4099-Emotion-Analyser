import React, { Component } from "react"
import { Paper, Table, TableBody, TableRow, TableCell } from "@material-ui/core"

class AUTable extends Component {
  constructor(props) {
    super(props)
    this.state = {
      data: [],
    }
  }

  componentDidMount() {
    console.log("table mounted!")
  }

  componentDidUpdate(prevProps) {
    let newProps = this.props
    if (prevProps.id !== newProps.id) {
      let nonZero = []
      let au = newProps.data
      for (let key in au) {
        if (au[key] > 0) {
          nonZero.push({
            label: key,
            value: au[key],
          })
        }
      }
      nonZero.sort((a, b) => b.value - a.value)
      let i = 0
      let rows = []
      nonZero.forEach(e => {
        rows.push(this.createTable(i++, e.label, e.value))
      })
      this.setState({ data: [...rows] })
    }
  }

  createTable = (id, key, value) => {
    return { id, key, value }
  }

  render() {
    if (this.state.data === undefined || this.state.data.length === 0) {
      return (
        <Paper>
          <h2>No Data Yet. Start Analysis!</h2>
        </Paper>
      )
    } else {
      return (
        <Paper>
          <Table>
            <TableBody>
              {this.state.data.map(row => (
                <TableRow key={row.id}>
                  <TableCell component="th">{row.key}</TableCell>
                  <TableCell>{row.value}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )
    }
  }
}

export default AUTable
