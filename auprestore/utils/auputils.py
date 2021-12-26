import re

def get_namespace(tag_with_namespace):
    """Returns namespace of an XML tag with namespace.
    
    An XML tag with a namespace has the syntax `{[namespace]}[tag]`, like `{xml/doc}project`.
    """
    return re.search('{.*}', tag_with_namespace)[0][1:-1]

def remove_namespace(tag_with_namespace):
    """Returns actual XML tag without namespace.
    
    An XML tag with a namespace has the syntax `{[namespace]}[tag]`, like `{xml/doc}project`.
    """
    len_of_brackets = 2
    index_of_tag_start = len(get_namespace(tag_with_namespace))+len_of_brackets
    return tag_with_namespace[index_of_tag_start:]

def get_data_folder_name(root):
    """Returns name of the project data files (.au) folder.
    
    Parameters
    ----------
    root
        Root element of the project file (.aup) XML tree.
    
    Raises
    ------
    TypeError
        If `root` does not have the tag `project`.
    TypeError
        If `root` does not have the a `projname` attribute (which describes the data files folder name).
    """
    if not remove_namespace(root.tag) == "project":
        raise TypeError("AUP project file does not start with a project tag.")
    if not "projname" in root.attrib:
        raise TypeError("AUP project file does not contain project name.")
    return root.get("projname")

def get_data_files(root):
    """Returns a set of all data files (.au) referenced in project file (.aup).

    Parameters
    ----------
    root
        Root element of the project file (.aup) XML tree.
    
    The root element has the following syntax (attributes and other tags omitted):
        <project>
            <wavetrack>
                <waveclip>
                    <sequence>
                        <waveblock>
                            <simpleblockfile filename="xxxxxx.au"/>
                        </waveblock>
                        ...
                    </sequence>
                    ...
                </waveclip>
                ...
            </wavetrack>
            ...
        </project>
    """
    namespace = get_namespace(root.tag)
    return set([
        simpleblockfile.get('filename') for 
        simpleblockfile in 
        root.iter('{}simpleblockfile'.format('{'+namespace+'}'))
    ])