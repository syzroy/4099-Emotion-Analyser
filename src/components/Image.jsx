import React from "react";
import { StaticQuery, graphql } from "gatsby";
import Img from "gatsby-image";

const Image = () => (
  <StaticQuery
    query={graphql`
      query {
        placeholderImage: file(relativePath: { eq: "back.jpg" }) {
          childImageSharp {
            fluid(maxWidth: 4160) {
              ...GatsbyImageSharpFluid
            }
          }
        }
      }
    `}
    render={data => (
      <Img
        fluid={data.placeholderImage.childImageSharp.fluid}
        style={{
          position: "fixed",
          left: 0,
          top: 0,
          width: "100%",
          height: "100%",
          zIndex: "-1"
        }}
      />
    )}
  />
);
export default Image;
