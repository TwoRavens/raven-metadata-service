
//import '../pkgs/bootstrap4/css/bootstrap.min.css';

//import hopscotch from 'hopscotch';
import '../css/app.css';

import m from 'mithril';
import Header from '../common/views/Header';
import Datamart from "../common/TwoRavens/Datamart";



var root = document.body
var mithrilRoot = document.getElementById("mithrilRoot");


//m.render(testDiv, 'Generated from Mithril in "index.js"')

var Splash = {
        view: function() {
            return m("div",
                    m("a", {href: "#!/hello"}, "Enter!"),
                    m("hr"),
                    m("p", m("a", {href: "#!/search"}, "Search!")),
            )
        }
    }
    /*
    m.render(root, m("main", [
      m("h1", {class: "title"}, "My first app"),
      m("button", "A button"),
    ]))
    */
    var count = 0 // added a variable

    var Hello = {
        view: function() {
            return m("main", [
                m("h1", {class: "title"}, "My first app"),
                m("button", {onclick: function() {count++}}, count + " clicks"),
                m("hr"),
                m("div", m("a", {href: "#!/splash"}, "(back to splash)")),

            ])
        }
    }

    export let augmentState = {
        dataset: {
            keywords: []
        }
    };

    export let augmentResults = [];

    var DatamartSearchPage = {
        view: function() {
            return m("main", [
                m(DatamartPageHeader),
                m("hr"),
                m(Datamart, {
                  augmentState: augmentState,
                  augmentResults: augmentResults
                }),
            ])
        }
    }

    let username;
    let userlinks = [
          {title: "Log in", url: "the login url"},
          {title: "Sign up", url: "the signup url"}
      ];

  var DatamartPageHeader = {

      view: function() {
        return m("nav", m(Header, {
                image: '/static/images/TwoRavens.png',
                aboutText: 'UI that exercises the Datamart Search API.',
                attrsInterface: {style: {}}
            },
            m('div', {style: {'flex-grow': 1}}),
            m('h4#dataName[style=display: inline-block; margin: .25em 1em]',
                'Datamart Search'),
            m('div', {style: {'flex-grow': 1}}),
        ))
    }}

    //m.mount(root, Hello) mithrilRoot
    m.route(mithrilRoot, "/splash", {
        "/splash": Splash,
        "/hello": Hello,
        '/search': DatamartSearchPage,
    })
