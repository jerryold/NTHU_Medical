import vtk

def main():

    colors = vtk.vtkNamedColors()

    # source
    reader = vtk.vtkMetaImageReader()
    reader.SetFileName("frog.mhd")
    reader.Update()

    # filters

    # TODO Add a gaussian filter to the pipeline, of which radius=4 std=3.5 #
    # Hint: use vtk.vtkImageGaussianSmooth()                                #
    #########################################################################
    gaussian = vtk.vtkImageGaussianSmooth()
    gaussian.SetInputConnection(reader.GetOutputPort())
    gaussian.SetDimensionality(3)
    gaussian.SetRadiusFactor(4)
    gaussian.SetStandardDeviations(3.5, 3.5, 3.5)
    #########################################################################
    #                           END OF THE TODO                             #

    subsampler = vtk.vtkImageShrink3D()
    # TODO Re-route the connection after adding the gaussian filter         #
    #########################################################################
    subsampler.SetInputConnection(gaussian.GetOutputPort())
    #########################################################################
    #                           END OF THE TODO                             #
    subsampler.SetShrinkFactors(4, 4, 1)

    m_cubes = vtk.vtkMarchingCubes()
    m_cubes.SetInputConnection(subsampler.GetOutputPort())
    m_cubes.ComputeNormalsOff()
    m_cubes.ComputeScalarsOff()
    m_cubes.ComputeGradientsOff()
    m_cubes.SetValue(0, 20.5)

    normals = vtk.vtkPolyDataNormals()
    normals.SetInputConnection(m_cubes.GetOutputPort())
    normals.SetFeatureAngle(60.0)

    stripper = vtk.vtkStripper()
    stripper.SetInputConnection(normals.GetOutputPort())

    # mappers
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(stripper.GetOutputPort())

    # actors
    skin_actor = vtk.vtkActor()
    skin_actor.SetMapper(mapper)
    skin_actor.GetProperty().SetColor(colors.GetColor3d("LimeGreen"))
    skin_actor.GetProperty().SetOpacity(.4)

    # renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(skin_actor)

    # render window
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(640, 480)
    render_window.Render()

    # interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    interactor.Start()

if __name__ == '__main__':
    main()
