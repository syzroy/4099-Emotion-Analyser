import React from "react"
import { Link } from "gatsby"

const IndexPage = () => (
  <div className={"index"}>
    <h1>Hi people</h1>
    <p>Welcome to your new Gatsby site.</p>
    <p>Now go build something great.</p>
    <Link to="/camera">Go to Camera</Link>
    <Link to="/video">Go to Video</Link>
  </div>
)

export default IndexPage
