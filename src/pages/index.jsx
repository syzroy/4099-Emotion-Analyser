import React from "react";
import { Link } from "gatsby";
import Image from "../components/Image";
import "../styles/layout.css";

const IndexPage = () => (
  <section>
    <Image />
    <div style={{ paddingTop: "20vh", paddingLeft: "10vw" }}>
      <h1>Emotion Analysis</h1>
    </div>
    <div style={{ paddingLeft: "10vw", paddingTop: "5vh" }}>
      <Link to="/camera" className="button">
        Go to Camera
      </Link>
      <Link to="/video" className="button">
        Go to Video
      </Link>
    </div>
  </section>
);

export default IndexPage;
