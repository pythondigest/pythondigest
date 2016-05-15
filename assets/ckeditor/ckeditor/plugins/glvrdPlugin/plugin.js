var glvrdPlugin_url = 'http://api.glvrd.ru/v1/glvrd.js';

if (!window.glvrd) {
    $.getScript(glvrdPlugin_url, function () { console.log ('api is loaded' ) });
}


function getCaretCharacterOffsetWithin(element) {
    var caretOffset = 0;
    var doc = element.ownerDocument || element.document;
    var win = doc.defaultView || doc.parentWindow;
    var sel;
    if (typeof win.getSelection != "undefined") {
        sel = win.getSelection();
        if (sel.rangeCount > 0) {
            var range = win.getSelection().getRangeAt(0);
            var preCaretRange = range.cloneRange();
            preCaretRange.selectNodeContents(element);
            preCaretRange.setEnd(range.endContainer, range.endOffset);
            caretOffset = preCaretRange.toString().length;
        }
    } else if ( (sel = doc.selection) && sel.type != "Control") {
        var textRange = sel.createRange();
        var preCaretTextRange = doc.body.createTextRange();
        preCaretTextRange.moveToElementText(element);
        preCaretTextRange.setEndPoint("EndToEnd", textRange);
        caretOffset = preCaretTextRange.text.length;
    }
    return caretOffset;
}


var glvrdPlugin =
{
    editor: '',
    name: "glvrdPlugin",
    title: "glvrdPlugin",
    tooltip: "glvrdPlugin",
    toolbar: 'glvrdPlugin',
    icon: "glvrdPlugin",
    targetWnd: {
        "id": "glvrd_results",
        "name" : "glvrd_name",
        "description": "glvrd_description"
    },
    context_title: "glvrdPlugin",
    exec: function (editor) {
        this.editor = editor;
        this.ruleset = {};
        var data = editor.getSnapshot();
        editor.element.data("text", data);

        glvrd.getStatus(function(r) {
            if ( r!== undefined && r.status =='ok')
            {
                result = glvrdPlugin.proofRead(data);
            }
        });
    },

    setText: function(text) {
        this.editor.loadSnapshot(text);
    },

    stripRuleTags: function(text)
    {
        var reg = /(<em[^>]*data-rule="r\d+"[^>]*>).+?(<\/em>)/g;
        return text.replace(reg,'');
    },

    proofRead: function(data) {

        window.glvrd.proofread(
            glvrdPlugin.stripRuleTags( data ),
            function (result) {
            var offset = 0;
            $.each(result.fragments, function (k, v) {
                var ruleName = 'r' + k;
                var tagStart = '<em class="glvrd-underline" data-rule="' + ruleName + '">';
                var tagClose = '</em>';

                var offsetLen = tagStart.length + tagClose.length;

                data = data.substring(0,v.start+offset)
                    + tagStart + data.substring(v.start+offset, v.end+offset)
                    + tagClose + data.substring(v.end+offset, data.length);
                offset += offsetLen;
                glvrdPlugin.ruleset[ruleName] = v.hint;
            });
            glvrdPlugin.setText(data);
            glvrdPlugin.registerHover(glvrdPlugin.ruleset);
        });
    },

    registerHover: function(ruleset) {
        var ckTextFrameName = CKEDITOR.instances[Object.keys(CKEDITOR.instances)[0]].id + '_contents iframe';
        var target = $('#' + ckTextFrameName).contents();
        $.each(ruleset, function(k,v){
            var emTarget = target.find('em').filter('[data-rule="'+ k + '"]');
            emTarget.on('mouseenter', function(e){
                $('#'+glvrdPlugin.targetWnd.name).html( ruleset[k].name );
                $('#'+glvrdPlugin.targetWnd.description).html( ruleset[k].description );
                $(this).addClass('glvrd-underline-active');
            }).on('mouseleave', function(e) {
                $(this).removeClass('glvrd-underline-active');
            });
            glvrdPlugin.trackChanges(emTarget,v);
        });
    },
    trackChanges: function(target,ruleItem) {
        target.on('DOMSubtreeModified', function(e){
                //console.debug( this.innerHTML );
        });
    },
    // todo: fire partial text update if no changes has been made to specified target within X seconds
    textTimeUpdate: function(time, position) {

    },
    inlineHints: function (target, data) {

    }
};


CKEDITOR.plugins.add('glvrdPlugin', {
    icons: 'glvrdPlugin',
    init: function (editor) {
        console.log('glvrd loaded');
        editor.addContentsCss( CKEDITOR.plugins.getPath( 'glvrdPlugin' ) + 'styles/glvrd.css' );
        editor.addCommand('glvrdPlugin', {
            exec: function (editor) {
                glvrdPlugin.exec(editor);
                //var now = new Date();
                //editor.insertHtml('The current date and time is: <em>' + now.toString() + '</em>');
            }
        });
        editor.ui.addButton(glvrdPlugin.name, {
            label: glvrdPlugin.title,
            command: glvrdPlugin.name,
            toolbar: glvrdPlugin.toolbar
        });

    }
});