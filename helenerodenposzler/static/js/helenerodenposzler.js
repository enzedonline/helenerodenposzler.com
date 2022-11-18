$(document).ready(function(){
    $('a[href^="http://"]').attr('target', '_blank');
    $('a[href^="http://"]').attr('rel', 'nofollow noopener');
    $('a[href^="https://"]').attr('target', '_blank');
    $('a[href^="https://"]').attr('rel', 'nofollow noopener');
});  

const addLangLinks = (linksID) => {
    const links = JSON.parse(document.getElementById(linksID).textContent);
    if (links) {
        for (const link of links) {
            linkElement = document.createElement('link');
            linkElement.rel = "alternate";
            linkElement.hreflang = link.hreflang;
            linkElement.href = link.href;
            document.head.append(linkElement);
        }
    }
}
{/* <link rel="alternate" hreflang="fr" href="https://helenerodenposzler.com/fr/"></link> */}
{/* <link rel="alternate" hreflang="x-default" href="https://helenerodenposzler.com/en/"></link> */}